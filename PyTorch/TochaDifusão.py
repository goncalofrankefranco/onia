import os
from numpy import uint8
from math import log
from scipy.io import loadmat
from PIL.Image import open
import matplotlib.pyplot as plt
import torch
from torch.utils.data import Dataset, DataLoader, ConcatDataset
from torchvision import transforms
from tqdm import tqdm

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# DATA PROCESSING
class KaggleCars(Dataset):
    def __init__(self, img_dir, mat_file, transform=None):
        self.img_dir, self.transform = img_dir, transform
        self.data = loadmat(mat_file)['annotations'][0]

    def __len__(self): return len(self.data)

    def __getitem__(self, i):
        img = open(os.path.join(self.img_dir, self.data[i]['fname'][0])).convert('RGB')
        if 'class' in self.data[i].dtype.names:
            label = int(self.data[i]['class'][0][0]) - 1
        else:
            label = -1
        return self.transform(img) if self.transform else img, label

def visualize(data):
    plt.figure(figsize=(15,15))
    for i, item in enumerate(data):
        if i == 20:
            break
        plt.subplot(6, 4, i+1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(item[0].permute(1,2,0))
    plt.show()

# FORWARD PROCESS - Noise Scheduler
def linear_beta_schedule(timesteps=200, start=0.0001, end=0.02):
    return torch.linspace(start, end, timesteps) # Returns 1D tensor [0.0001, 0.0002... 0.002]

def get_index_from_list(vals, t, x_shape):
    batch_size = t.shape[0]
    out = vals.gather(-1, t)
    return out.reshape(batch_size, *((1,) * (len(x_shape) - 1)))

def forward_distribution_sample(x_0, t): # Takes an image and returns the noisy version of it
    noise = torch.randn_like(x_0)
    sqrt_alphas_cumprod_t = get_index_from_list(sqrt_alphas_cumprod, t, x_0.shape)
    sqrt_one_minus_alphas_cumprod_t = get_index_from_list(sqrt_one_minus_alphas_cumprod, t, x_0.shape)
    # Mean + Variance
    return  sqrt_alphas_cumprod_t * x_0 + sqrt_one_minus_alphas_cumprod_t * noise, noise

# SHOWING
def show_tensor_image(image):
    reverse_transforms = transforms.Compose([
    transforms.Lambda(lambda t: (t + 1) / 2),
    transforms.Lambda(lambda t: t.permute(1, 2, 0)),
    transforms.Lambda(lambda t: t * 255),
    transforms.Lambda(lambda t: t.numpy().astype(uint8)),
    transforms.ToPILImage(),
    ])

    if len(image.shape) == 4:
        image = image[0, :, :, :]
        image = image.cpu()
    plt.imshow(reverse_transforms(image))


def show_transformation():
    image = next(iter(dataloader))[0]
    plt.figure(figsize=(20,3))
    plt.axis('off')
    num_images = 10

    for idx in range(0, num_images):
        t = torch.Tensor([int(T / num_images * idx)]).type(torch.int64)
        plt.subplot(1, num_images+1, idx + 1) # Rows, Columns, Index
        img, noise = forward_distribution_sample(image, t)
        show_tensor_image(img)
        plt.axis('off')
    plt.show()

# BACKWARD PROCESS - U-Net
class SimpleUNet(torch.nn.Module):
    # DEFINITIONS
    def __init__(self):
        super().__init__()
        image_size = 64
        image_channels = 3
        down_channels = [64, 128, 256, 512, 1024]
        up_channels = [1024, 512, 256, 128, 64]
        out_dimension = 1
        time_embed_dimension = 32

        # Timestep Embedding Model
        self.time_mlp = torch.nn.Sequential(
            SinusoidalPositionalEmbedding(time_embed_dimension), # Positional embedding
            torch.nn.Linear(time_embed_dimension, time_embed_dimension),
            torch.nn.ReLU()
        )

        # Setting up CNN to downscale image
        self.conv0 = torch.nn.Conv2d(image_channels, down_channels[0], 3, padding=1)

        # Downscaling loop
        self.downs = torch.nn.ModuleList([Block(down_channels[i], down_channels[i + 1],time_embed_dimension) \
                                        for i in range(len(down_channels) - 1)])

        # Upscaling loop
        self.ups = torch.nn.ModuleList([Block(up_channels[i], up_channels[i + 1], time_embed_dimension, up=True) \
                                        for i in range(len(up_channels) - 1)])

        # Reverse CNN to convert to output
        self.output = torch.nn.Conv2d(up_channels[-1], 3, out_dimension)

    def forward(self, x, timestep):
        t = self.time_mlp(timestep) # Embedding time
        x = self.conv0(x) # Initial CNN
        residual_inputs = []
        # U-Net
        for down in self.downs:
            x = down(x, t)
            residual_inputs.append(x)
        for up in self.ups:
            residual_x = residual_inputs.pop()
            # Add residual x as aditional channels
            x = torch.cat((x, residual_x), dim=1)
            x = up(x, t)
        return self.output(x)

class SinusoidalPositionalEmbedding(torch.nn.Module):
    def __init__(self, dimension):
        super().__init__()
        self.dimension = dimension

    def forward(self, time):
        device = time.device
        half_dimension = self.dimension / 2
        embeddings = log(10000) / half_dimension # do half_dimension - 1 if publishing, it's a standard bug
        embeddings = torch.exp(torch.arange(half_dimension, device=device) * -embeddings) # e^[1, 2... half_dimension] manipulated by -embeddings
        embeddings = time[:, None] * embeddings[None, :] # Combines timesteps with frequencies, scaling wavelengths up based on step
        embeddings = torch.cat((embeddings.sin(), embeddings.cos()), dim=-1) # Makes the waaaaves
        return embeddings

class Block(torch.nn.Module):
    # DEFINITIONS
    def __init__(self, in_channels, out_channels, time_embed_dimension, up=False):
        super().__init__()
        self.time_mlp = torch.nn.Linear(time_embed_dimension, out_channels)
        # Conv2d = CNN Downsampling - ConvTranspose2d = CNN Upsampling
        if up:
            self.conv1 = torch.nn.Conv2d(2*in_channels, out_channels, 3, padding=1)
            self.transform = torch.nn.ConvTranspose2d(out_channels, out_channels, 4, stride=2, padding=1)
        else:
            self.conv1 = torch.nn.Conv2d(in_channels, out_channels, 3, padding=1)
            self.transform = torch.nn.Conv2d(out_channels, out_channels, 4, stride=2, padding=1)

        self.conv2 = torch.nn.Conv2d(out_channels, out_channels, 3, padding=1)
        self.bnorm1 = torch.nn.BatchNorm2d(out_channels)
        self.bnorm2 = torch.nn.BatchNorm2d(out_channels)
        self.relu = torch.nn.ReLU()

    def forward(self, x, t):
        h = self.bnorm1(self.relu(self.conv1(x))) # First CNN
        time_embedding = self.relu(self.time_mlp(t))
        time_embedding = time_embedding[(..., ) + (None, ) * 2] # Adapt time_embedding to match h (current dimension + torch.unsqueeze() 2 times)
        h += time_embedding
        h = self.bnorm2(self.relu(self.conv2(h)))
        return self.transform(h)

# LOSS FUNCTION - (Actual noise - Predicted noise)^2
def get_loss(model, x_0, t):
    x_noisy, noise = forward_distribution_sample(x_0, t)
    noise_pred = model(x_noisy, t)
    return torch.nn.functional.l1_loss(noise, noise_pred) # l1 = linear, MSE = quadratic

# SAMPLING - Actually runs the model
@torch.no_grad()
def sample_timestep(x, t):
    """ Calls the model to predict the noise in the image and returns the denoised image.
    Applies noise to the image if it isn't in the last step yet. """
    betas_t = get_index_from_list(betas, t, x.shape) # Gets betas on t steps
    sqrt_one_minus_alphas_cumprod_t = get_index_from_list(sqrt_one_minus_alphas_cumprod, t, x.shape)
    sqrt_recip_alphas_t = get_index_from_list(sqrt_recip_alphas, t, x.shape)

    # Call model (current image - noise prediction)
    model_mean = sqrt_recip_alphas_t * (x - betas_t * model(x, t) / sqrt_one_minus_alphas_cumprod_t)
    posterior_variance_t = get_index_from_list(posterior_variance, t, x.shape)

    if t != 0:
        noise = torch.randn_like(x) # Numbers between [-1, 1]
        return model_mean + torch.sqrt(posterior_variance_t) * noise
    else:
        return model_mean

@torch.no_grad()
def sample_plot_image(epoch, step_idx):
    img_size = 64
    img = torch.randn((1, 3, img_size, img_size), device=device)
    fig = plt.figure(figsize=(15, 15))
    plt.axis('off')
    num_images = 10
    stepsize = T/num_images

    for step in tqdm(range(T)[::-1], desc="Visualizing"):
        t = torch.full((1,), step, device=device).long() # Tensor full of fill values. (1,) is a tuple
        img = sample_timestep(img, t)
        img = torch.clamp(img, -1., 1.) # Maintains the natural range of distribution
        if step % stepsize == 0:
            plt.subplot(1, num_images, int(step/stepsize) + 1)
            show_tensor_image(img.detach().cpu()) # Detach to remove calculus bs data so plt accepts it
    plt.savefig(f"Difussion epoch {epoch} step {step_idx}.png")
    plt.close(fig)

# ACTUAL CODE START
if __name__ == '__main__': # Prevents workers loop
    data_transforms = [
        transforms.Resize((64, 64)),
        transforms.RandomHorizontalFlip(), # Data augmentation
        transforms.ToTensor(), # Scales data between [0, 1]
        #transforms.Lambda(lambda t: (t * 2) - 1) # Scale between [-1, 1] - PAUSED DO TO PICKLING ERROR
    ]

    data_transform = transforms.Compose(data_transforms) # Combines the transforms

    train_data = KaggleCars(
        img_dir='C:/Codigos_mt_legais/RushadãoPythonPqSim/ONIA/Data/cars_train/cars_train',
        mat_file='C:/Codigos_mt_legais/RushadãoPythonPqSim/ONIA/Data/car_devkit/devkit/cars_train_annos.mat',
        transform=data_transform
    )

    test_data = KaggleCars(
        img_dir='C:/Codigos_mt_legais/RushadãoPythonPqSim/ONIA/Data/cars_test/cars_test',
        mat_file='C:/Codigos_mt_legais/RushadãoPythonPqSim/ONIA/Data/car_devkit/devkit/cars_test_annos.mat',
        transform=data_transform
    )

    # DEFINITIONS
    T = 200
    betas = linear_beta_schedule(T)

    # PRECALCULATIONS
    betas = linear_beta_schedule(T).to(device)
    alphas = (1. - betas).to(device)
    alphas_cumprod = torch.cumprod(alphas, axis=0).to(device) # cumprod = cumulative product
    alphas_cumprod_prev = torch.nn.functional.pad(alphas_cumprod[:-1], (1, 0), value=1.0).to(device) # Adds padding for CNN to maintain res
    sqrt_recip_alphas = torch.sqrt(1. / alphas).to(device)
    sqrt_alphas_cumprod = torch.sqrt(alphas_cumprod).to(device)
    sqrt_one_minus_alphas_cumprod = torch.sqrt(1. - alphas_cumprod).to(device)
    posterior_variance = (betas * (1. - alphas_cumprod_prev) / (1. - alphas_cumprod)).to(device) # Backward prediction ratio

    # DATA
    batch_size = 64
    data = ConcatDataset([train_data, test_data])
    dataloader = DataLoader(data, batch_size=batch_size, shuffle=True, drop_last=True,
                            num_workers=2, pin_memory=True, persistent_workers=True)

    model = SimpleUNet()

    # TRAINING
    model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    epochs = 100

    for epoch in tqdm(range(epochs), desc='Epoch'):
        for step_idx, batch in tqdm(enumerate(dataloader), desc='Step'):
            optimizer.zero_grad(set_to_none=True) # Resetting gradients, not disabling

            batch_0 = batch[0].to(device)
            batch_0 = (batch_0 * 2) - 1 # Substitute to lambda function
            t = torch.randint(0, T, (batch_size,), device=device).long() #.long() = .to(int64)
            loss = get_loss(model, batch_0, t)
            loss.backward()
            optimizer.step()

            if epoch % 5 == 0 and step_idx == 0:
                print(f"\nEpoch {epoch} | step {step_idx:03d} Loss: {loss.item()} ")
                #sample_plot_image(epoch, step_idx)

    torch.save(model.state_dict(), './difussion_model.pth')


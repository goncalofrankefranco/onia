from torch import nn, optim
from torch.utils.data import Dataset, DataLoader
from torchvision.datasets import ImageFolder
from torchvision.transforms import transforms
import lightning as L
from inspect import signature

train_dataset = ImageFolder(root='C:\\Codigos_mt_legais\\RushadãoPythonPqSim\\ONIA\\Data\\archive\\seg_train', transform=transforms.ToTensor())
test_dataset = ImageFolder(root='C:\\Codigos_mt_legais\\RushadãoPythonPqSim\\ONIA\\Data\\archive\\seg_test', transform=transforms.ToTensor())

train_loader = DataLoader(dataset=train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(dataset=test_dataset, batch_size=32, shuffle=True)

class ImageClassifier(L.LightningModule):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Conv2d(3 * pow(224, 2), out_channels=128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(128, out_channels=256, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

    def forward(self, x):
        x = self.model(x)
        return x

    def configure_optimizers(self):
        optimizer = optim.Adam(self.model.parameters())

model = ImageClassifier()
trainer = L.Trainer(
    max_epochs=10,
    accelerator='gpu',
    devices=1,
    precision=16
)

trainer.fit(model, train_loader)
print(trainer.test(model, test_loader))
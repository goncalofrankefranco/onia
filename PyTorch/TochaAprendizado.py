import torch
import torch.nn as nn
import torch.optim as optim
#from torch.testing._internal.distributed.rpc import rpc_agent_test_fixture
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
import timm

import matplotlib.pyplot as plt
#import numpy as np
#import pandas as pd
from tqdm import tqdm

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# DATASET: formatting setup
class PlayingCardDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        self.data = ImageFolder(data_dir, transform=transform)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

    @property
    def classes(self):
        return self.data.classes

# Train dataset setup and formatting
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

train_dataset = PlayingCardDataset(data_dir="./archive/train", transform=transform)
test_dataset = PlayingCardDataset(data_dir="./archive/test", transform=transform)
val_dataset = PlayingCardDataset(data_dir="./archive/valid", transform=transform)



# Iteration
"""
for image, label in dataset:
    print(image)
"""

# DATALOADER: Batching setup
train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=32, shuffle=True)
val_dataloader = DataLoader(val_dataset, batch_size=32, shuffle=True)


# MODEL: Setup
class SimpleCardClassifier(nn.Module):
    def __init__(self, num_classes=53):
        super().__init__()
        # Defining Parts
        self.base_model = timm.create_model('efficientnet_b0', pretrained=True, num_classes=0)
        enet_out_size = 1280

        # Making a classifier
        self.classifier = nn.Linear(enet_out_size, num_classes)

    def forward(self, x):
        # Connecting the parts
        x = self.base_model(x)
        output = self.classifier(x)
        return output

# Assigning model
model = SimpleCardClassifier(num_classes=53)
model.to(device)

# Output example
train_images, train_labels = next(iter(train_dataloader))
train_images, train_labels = train_images.to(device), train_labels.to(device)
example_out = model(train_images)
#print(example_out)

# LOSS FUNCTION: Setup
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
#print(criterion(example_out, labels))

# TRAINING LOOP: Setup
num_epochs = 5
train_losses, val_losses = [], []
for epoch in range(num_epochs):
    # Training phase
    model.train()
    running_loss = 0.0
    for images, labels in tqdm(train_dataloader, desc='Training Loop'):
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad() # Clean gradients
        outputs = model(images) # Test model
        loss = criterion(outputs, labels) # Calculate loss
        loss.backward() # Computes new gradients
        optimizer.step() # Backpropagates them
        running_loss += loss.item() * images.size(0) # Average loss 1/2
    train_loss = running_loss / len(train_dataset) # Average loss 2/2
    train_losses.append(train_loss)

    #Validation phase
    model.eval()
    running_loss = 0.0
    with torch.no_grad():
        for images, labels in tqdm(val_dataloader, desc='Validation Loop'):
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)  # Test model
            loss = criterion(outputs, labels)  # Calculate loss
            running_loss += loss.item() * images.size(0)
        val_loss = running_loss / len(val_dataset)
        val_losses.append(val_loss)

    # Print epoch stats:
    print(f"Epoch {epoch+1}/{num_epochs}, Train Loss: {train_loss}, Validation Loss: {val_loss}")

plt.plot(train_losses, label="Training loss")
plt.plot(val_losses, label="Validation loss")
plt.show()
torch.save(model.state_dict(), "modelo_cartas_v1.pth")
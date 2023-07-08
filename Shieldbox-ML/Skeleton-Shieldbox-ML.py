import os
import pandas as pd
from pathlib import Path
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.datasets as datasets
from torchvision.io import read_image
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, random_split

class CustomImageDataset():
    def __init__(self, img_dir, transform=None, target_transform=None):
        self.img_dir = img_dir
        self.images = []
        for filename in os.listdir(img_dir):
          if os.path.isfile(os.path.join(img_dir, filename)):
            self.images.append(filename)
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        name = self.images[idx]
        img_path = os.path.join(self.img_dir, name)
        image = read_image(img_path)
        label = Path(img_path).stem
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, label

# Define the neural network architecture
class DigitClassifier(nn.Module):
    def __init__(self, n, m):
        super(DigitClassifier, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1) #will need to play with numbers
        self.relu = nn.ReLU()
        self.maxpool = nn.MaxPool2d(kernel_size=2, stride=2) #2 x 2
        self.fc = nn.Linear(32 * n * m, 7 * 10)  # 7x7 is the size of the image after max pooling, play with numbers

    def forward(self, x):
        x = self.conv1(x) #first layer
        x = self.relu(x) #make negatives zero?
        x = self.maxpool(x) #takes little window and outputs max in window
        x = x.view(x.size(0), -1)  # flatten the tensor
        x = self.fc(x)
        x = x.view(7,10)
        torch.clip(x, min=0, max=1)
        return x

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def transformer(label): #turns string into what we want
  label = [int(x) for x in label]
  label = torch.tensor(label)
  return F.one_hot(label, num_classes=10)

h = 475
w = 475

def im_transformer(x):
  x = transforms.ToTensor()(x)
  x = transforms.Resize((3,h,w))
  return x

# Load MNIST dataset
dataset = CustomImageDataset("/content/ML/shieldbox", transform=transforms.Lambda(im_transformer), target_transform=transforms.Lambda(transformer)) #/content/ML/shieldbox is wherever the cropped images are living
train, test = random_split(dataset, [0.2, 0.8])
# Data loaders
batch_size = 64 #set to actual value
train_loader = DataLoader(dataset=train, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(dataset=test, batch_size=batch_size, shuffle=False)

# Create the model
model = DigitClassifier(h,w).to(device)

# Define loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 10
for epoch in range(num_epochs):
    for batch_idx, (data, targets) in enumerate(train_loader):
        # Move data to device
        data = data.to(device=device)
        targets = targets.to(device=device)

        # Forward pass
        scores = model(data)
        loss = criterion(scores, targets)

        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    # Print loss for each epoch
    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {loss.item()}")

# Evaluate the model
def evaluate(model, data_loader):
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for data, targets in data_loader:
            data = data.to(device=device)
            targets = targets.to(device=device)

            scores = model(data)
            _, predictions = scores.max(1)
            correct += (predictions == targets).sum()
            total += targets.size(0)

    model.train()
    return correct.item() / total

def testing(evaluation, total):

# Test the model
train_accuracy = evaluate(model, train_loader)
test_accuracy = evaluate(model, test_loader)

print(f"Train Accuracy: {train_accuracy*100:.2f}%")
print(f"Test Accuracy: {test_accuracy*100:.2f}%")

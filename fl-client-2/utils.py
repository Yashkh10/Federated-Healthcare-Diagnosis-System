from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import os

def load_data(data_dir="data"):
    transform = transforms.Compose([
        transforms.Grayscale(),  
        transforms.Resize((32, 32)),  
        transforms.ToTensor(),
    ])

    train_path = os.path.join(data_dir, "train")
    test_path = os.path.join(data_dir, "test")

    train_dataset = datasets.ImageFolder(train_path, transform=transform)
    test_dataset = datasets.ImageFolder(test_path, transform=transform)

    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=8, shuffle=False)
    return train_loader, test_loader

import flwr as fl
import torch
import torch.nn as nn
import torch.optim as optim
from model import CNN
from utils import load_data
import os

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = CNN().to(DEVICE)

try:
    train_loader, test_loader = load_data()
except FileNotFoundError as e:
    print("❌", e)
    exit(1)

loss_fn = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

def train():
    model.train()
    for data, target in train_loader:
        data, target = data.to(DEVICE), target.to(DEVICE)
        optimizer.zero_grad()
        output = model(data)
        loss = loss_fn(output, target)
        loss.backward()
        optimizer.step()

def test():
    model.eval()
    correct, total = 0, 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(DEVICE), target.to(DEVICE)
            output = model(data)
            pred = output.argmax(dim=1)
            correct += pred.eq(target).sum().item()
            total += target.size(0)
    return correct / total

class FlowerClient(fl.client.NumPyClient):
    def get_parameters(self, config):
        return [val.cpu().numpy() for val in model.state_dict().values()]

    def set_parameters(self, parameters):
        params_dict = zip(model.state_dict().keys(), parameters)
        model.load_state_dict({k: torch.tensor(v) for k, v in params_dict}, strict=True)

    def fit(self, parameters, config):
        round_num = config.get("rnd", "?")
        msg = f"[Client] Training round {round_num}"
        print(f"{msg} - started...")
        self.set_parameters(parameters)
        train()
        print(f"{msg} - finished.")
        return self.get_parameters(config), len(train_loader.dataset), {}

    def evaluate(self, parameters, config):
        print("[Client] Evaluating model...")
        self.set_parameters(parameters)
        acc = test()
        print(f"[Client] Evaluation accuracy: {acc:.4f}")
        return float(1.0 - acc), len(test_loader.dataset), {"accuracy": acc}

if __name__ == "__main__":
    fl.client.start_numpy_client(server_address="fl-server:8080", client=FlowerClient())

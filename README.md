# Federated Healthcare Diagnosis System (FL + Blockchain)

This project demonstrates a federated learning system for collaborative medical diagnosis, integrated with public blockchain (Ethereum using Ganache) for immutable audit logging. It allows multiple clients (e.g., hospitals) to train a CNN on local medical image data (e.g., X-rays) without sharing raw patient data.

## 🔍 Use Case

Hospitals collaboratively train a deep learning model to detect diseases like pneumonia from X-ray images. Patient data stays local, and only model updates are shared. Blockchain ensures a tamper-proof log of model training rounds.

---

## 📁 Folder Structure

```
.
├── fl-server/               # Federated learning server (Flower)
│   └── server.py
├── fl-client-1/             # First FL client
│   ├── client.py
│   ├── model.py
│   ├── utils.py
│   └── data/                # Local training data (train/test folders)
├── fl-client-2/             # Second FL client (same structure as client-1)
├── contracts/               # Smart contract for training log
│   └── TrainerLog.sol
├── fabric-api/              # Node.js API to log FL data to blockchain
│   ├── index.js
│   └── contract/
│       └── config.js
├── truffle-config.js        # Truffle setup for contract deployment
├── docker-compose.yml       # All services orchestrated via Docker
```

---

## ⚙️ Technologies Used

* **Federated Learning Framework**: [Flower](https://flower.dev)
* **Deep Learning**: PyTorch
* **Blockchain**: Ethereum (local Ganache), Solidity, Truffle
* **API**: Node.js (Express)
* **Orchestration**: Docker Compose

---

## 🧠 Model Architecture

`model.py`

```python
class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.fc1 = nn.Linear(32 * 8 * 8, 128)
        self.fc2 = nn.Linear(128, 2)  # Binary classification
```

---

## 🔁 What Happens When You Run It?

1. The **Flower server** starts listening for clients and aggregates their model updates.
2. Each **client** trains the model locally and sends updated weights.
3. After each round, the **server logs accuracy, loss, and timestamp** to the blockchain via the `fabric-api`.
4. `TrainerLog.sol` contract records these logs immutably.

**Example Console Output (from Server):**

```
[Round 1] Avg Accuracy: 0.86, Logging to Fabric API...
✅ Logged to blockchain via Fabric API.
```

**Example Console Output (from Client):**

```
[Client] Training round 1 - started...
[Client] Training round 1 - finished.
[Client] Evaluation accuracy: 0.8600
```

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/sumity2021/federated-healthcare.git
cd federated-healthcare
```

### 2. Deploy Smart Contract

```bash
cd contracts
truffle migrate --network development
```

Update the deployed contract address in `fabric-api/contract/config.js`.

### 3. Start All Services via Docker

```bash
docker-compose up --build
```

This runs:

* Federated Learning server (`fl-server`)
* Two clients (`fl-client-1`, `fl-client-2`)
* Node.js API (`fabric-api`)
* Ganache blockchain simulator

---

## 📝 Sample Smart Contract: `TrainerLog.sol`

```solidity
event RoundLogged(uint256 round, string accuracy, string loss, uint256 timestamp);
function logTrainingRound(...) public { ... }
```

Logs training rounds with accuracy and loss per round.

---

## 📡 API Endpoint

`POST /log-round`

```json
{
  "round": 1,
  "accuracy": 0.86,
  "loss": 0.34,
  "timestamp": 1720000000
}
```

---

## 📷 Data Format

Each client must have a dataset in this format:

```
data/
├── train/
│   ├── class0/
│   └── class1/
└── test/
    ├── class0/
    └── class1/
```

---

## 📌 Notes

* Data is assumed to be grayscale images (e.g., chest X-rays).
* Accuracy and loss are converted to strings in blockchain logs due to Solidity limitations.

---

## 📬 Contributors

* Sumit Yadav — [GitHub](https://github.com/sumity2021)
* Yash Khandelwal - [GitHub](https://github.com/Yashkh10)
* Arunabh Shikhar -[GitHub](https://github.com/ArunabhShikhar10717)

---

## 🛡️ License

MIT License

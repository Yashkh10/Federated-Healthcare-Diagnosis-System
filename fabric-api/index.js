const express = require("express");
const bodyParser = require("body-parser");
const { web3, contract } = require("./contract/config");

const app = express();
const PORT = 3000;

app.use(bodyParser.json());

app.post("/log-round", async (req, res) => {
  const { round, accuracy, loss, timestamp } = req.body;

  if (round == null || accuracy == null || loss == null || timestamp == null) {
    return res.status(400).send({ error: "Missing parameters" });
  }

  try {
    const accounts = await web3.eth.getAccounts();
    const tx = await contract.methods
      .logTrainingRound(round, accuracy.toFixed(4), loss.toFixed(4), timestamp)
      .send({ from: accounts[0], gas: 200000 });

    console.log(
      `✅ Logged round ${round} to blockchain. TX: ${tx.transactionHash}`
    );
    res
      .status(200)
      .send({ message: "Logged to blockchain", tx: tx.transactionHash });
  } catch (err) {
    console.error("❌ Blockchain logging error:", err);
    res.status(500).send({ error: "Blockchain logging failed" });
  }
});

app.listen(PORT, () => {
  console.log(`fabric-api running on http://localhost:${PORT}`);
});

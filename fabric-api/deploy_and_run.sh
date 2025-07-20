

echo "🚀 Deploying smart contract..."
cd ./blockchain

OUT=$(truffle migrate --network development --reset)

ADDR=$(echo "$OUT" | grep "contract address:" | awk '{print $4}')

if [ -z "$ADDR" ]; then
  echo "❌ Deployment failed: no address found"
  exit 1
fi

echo "✅ Contract deployed at: $ADDR"

cd ../contract
sed -i "s/const contractAddress = \".*\";/const contractAddress = \"$ADDR\";/" config.js

cd ..
echo "🚦 Starting fabric-api..."
node index.js

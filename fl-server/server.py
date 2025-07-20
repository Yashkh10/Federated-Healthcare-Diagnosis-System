import flwr as fl
import requests
import time
from typing import List, Tuple, Dict, Optional

FABRIC_API_URL = "http://fabric-api:3000/log-round"

class LoggingFedAvg(fl.server.strategy.FedAvg):
    def __init__(self):
        super().__init__(
            evaluate_metrics_aggregation_fn=self.aggregate_accuracy,
            on_fit_config_fn=self.fit_config,  
        )

    @staticmethod
    def aggregate_accuracy(metrics_list):
        accuracies = [m["accuracy"] * n for n, m in metrics_list if "accuracy" in m]
        total = sum(n for n, m in metrics_list if "accuracy" in m)
        return {"accuracy": sum(accuracies) / total if total > 0 else 0.0}

    @staticmethod
    def fit_config(rnd: int) -> Dict[str, fl.common.Scalar]:
        return {"rnd": rnd}  

    def aggregate_evaluate(
        self,
        rnd: int,
        results: List[Tuple[fl.server.client_proxy.ClientProxy, fl.common.EvaluateRes]],
        failures: List[BaseException],
    ) -> Optional[Tuple[float, Dict[str, fl.common.Scalar]]]:

        aggregated_loss, aggregated_metrics = super().aggregate_evaluate(rnd, results, failures)

        accuracy = aggregated_metrics.get("accuracy") if aggregated_metrics else None
        timestamp = int(time.time())

        print(f"[Round {rnd}] Avg Accuracy: {accuracy}, Logging to Fabric API...")

        try:
            payload = {
                "round": rnd,
                "accuracy": accuracy,
                "loss": aggregated_loss,
                "timestamp": timestamp
            }
            print("Payload being sent:", payload)
            res = requests.post(FABRIC_API_URL, json=payload)
            res.raise_for_status()
            print("✅ Logged to blockchain via Fabric API.")
        except Exception as e:
            print("❌ Error logging to Fabric API:", str(e))

        return aggregated_loss, aggregated_metrics


if __name__ == "__main__":
    fl.server.start_server(
        server_address="0.0.0.0:8080",
        config=fl.server.ServerConfig(num_rounds=3),
        strategy=LoggingFedAvg(),
    )

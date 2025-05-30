# Evaluation du modèle
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, classification_report
import hydra
from omegaconf import DictConfig
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@hydra.main(config_path="../../configs", config_name="config", version_base="1.3") # type: ignore
def evaluate_model(cfg: DictConfig):
    """
    Main function to evaluate the model.
    """
    X = pd.read_csv(f"{cfg['paths']['processed_x']}")
    X_saved_train = pd.read_csv(f"{cfg['paths']['saved_training_data']}")
    X_validation = X[~X.date.isin(X_saved_train.date)]
    y_validation = X_validation.result
    X_validation.drop("result", inplace=True, errors="ignore")

    logging.info(f"Evaluating model {cfg["model"]["name"]} with {len(X_validation)} samples")
    model = joblib.load(cfg["model"]["output_path"])
    y_pred = model.predict(X_validation)

    print("Accuracy:", accuracy_score(y_validation, y_pred))
    print(classification_report(y_validation, y_pred))

if __name__ == "__main__":
    evaluate_model()
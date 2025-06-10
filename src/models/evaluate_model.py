# Evaluation du modèle
import mlflow.sklearn
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, classification_report
import hydra
from omegaconf import DictConfig
import logging
import mlflow
import mlflow.sklearn
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

    logging.info(f"Evaluating model {cfg['model']['name']} with {len(X_validation)} samples")
    mlflow.set_tracking_uri(cfg["tracking"]["mlflow_uri"])
    mlflow.set_experiment(cfg["model"]["experiment_name"])
    with mlflow.start_run():
        mlflow.log_param("model_name", cfg["model"]["name"])
        mlflow.log_param("Number of games this season", len(X_validation))
        mlflow.log_param("Most recent game", X_validation.date.max())
        model = joblib.load(cfg["model"]["output_path"])
        mlflow.sklearn.log_model(model, "model") # type: ignore
        
        mlflow.log_param("features", list(cfg["data"]["features"]))
        y_pred = model.predict(X_validation)
        accuracy = accuracy_score(y_validation, y_pred)
        classification_report_str = classification_report(y_validation, y_pred)
        mlflow.log_metric("accuracy", accuracy) # type: ignore
        mlflow.log_text(classification_report_str, "classification_report.txt") # type: ignore
        logging.info("Accuracy:", accuracy)
        logging.info(classification_report)
        logging.info("Model evaluation completed successfully.")

if __name__ == "__main__":
    evaluate_model()
import mlflow.sklearn
import mlflow.sklearn
import mlflow.sklearn
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pandas as pd
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import joblib
import logging
import mlflow
import mlflow.sklearn
import os
from sklearn.model_selection import cross_val_score
import bentoml

# Entraînement du modèle
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

import hydra
from omegaconf import DictConfig

@hydra.main(config_path="../../configs", config_name="config", version_base="1.3") # type: ignore

def train_model(cfg: DictConfig):
    """
    Main function to train the model.
    """
    model_path = f"{cfg['model']['output_path']}"

    
    preprocessor = Pipeline(steps=[
    ("preprocessor", ColumnTransformer(
        transformers=[
            ("keep_cols", "passthrough", list(cfg["data"]["features"])),

            
        ],
        remainder='drop'
    ))
    ])

    # Initialiser le modèle

    model_name = cfg["model"]["name"]
    if model_name == "xgboost":
        logging.info("Using XGBoost classifier")
        model = XGBClassifier(**cfg["model"]["parameters"])
    elif model_name == "lightgbm":
        logging.info("Using LightGBM classifier")
        model = LGBMClassifier(**cfg["model"]["parameters"])
    else:
        raise ValueError(f"Model {model_name} is not supported. Please choose 'xgboost' or 'lightgbm'.")
    
    pipeline_model = Pipeline([
    ("preprocess", preprocessor),
    ("model", model)
    ])
    X_processed = pd.read_csv(f"{cfg['paths']['processed_x']}")
    X_saved_train = pd.read_csv(f"{cfg['paths']['saved_training_data']}")
    X = X_processed[X_processed.date.isin(X_saved_train.date)]
    y = X[cfg["training"]["target_col"]]
    

    # X_validation = X[~X.date.isin(X_saved_train.date)]
    # y_validation = X_validation.result
    # X_validation.drop("result", inplace=True, errors="ignore")
    mlflow.set_tracking_uri(cfg["tracking"]["mlflow_uri"])
    mlflow.set_experiment(cfg["model"]["experiment_name"])
    with mlflow.start_run():
        mlflow.log_params(cfg["training"]["model_params"])
        mlflow.log_param("model_name", model_name)
        mlflow.log_param("features", list(cfg["data"]["features"]))
        logging.info(f"Training model with {len(X)} samples")
        cv_score = cross_val_score(pipeline_model, X, y, cv=5, scoring='accuracy')
        pipeline_model.fit(X, y)
        mlflow.sklearn.log_model(pipeline_model, "model") # type: ignore
        mlflow.log_metric("cross_val_score", cv_score.mean())
        mlflow.log_artifact(f"{cfg['paths']['processed_x']}", artifact_path="processed_data")
        logging.info(f"Cross-validation score: {cv_score.mean()}")
        os.makedirs(cfg["model"]["output_dir"], exist_ok=True)  # Crée le dossier s'il a été supprimé
        joblib.dump(pipeline_model, model_path)
        bentoml.sklearn.save_model(model_name, pipeline_model, signatures={
            "predict": {"batchable": True},
            "predict_proba": {"batchable": True}
        })
    logging.info(f"Model trained and saved to {model_path} with MLflow tracking")

if __name__ == "__main__":
    train_model()
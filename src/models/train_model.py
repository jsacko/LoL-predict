from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pandas as pd
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import joblib
import logging
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
        model = XGBClassifier(**cfg["training"]["model_params"])
    elif model_name == "lightgbm":
        logging.info("Using LightGBM classifier")
        model = LGBMClassifier(**cfg["training"]["model_params"])
    else:
        raise ValueError(f"Model {model_name} is not supported. Please choose 'xgboost' or 'lightgbm'.")
    
    pipeline_model = Pipeline([
    ("preprocess", preprocessor),
    ("model", model)
    ])
    X = pd.read_csv(f"{cfg["paths"]["processed_x"]}")
    X_saved_train = pd.read_csv(f"{cfg['paths']['saved_training_data']}")
    X_train = X[X.date.isin(X_saved_train.date)]
    y_train = X_train[cfg["training"]["target_col"]]
    # X_validation = X[~X.date.isin(X_saved_train.date)]
    # y_validation = X_validation.result
    # X_validation.drop("result", inplace=True, errors="ignore")
    logging.info(f"Training model with {len(X_train)} samples")
    pipeline_model.fit(X_train, y_train)
    joblib.dump(pipeline_model, model_path)
    logging.info(f"Model trained and saved to {model_path}")

if __name__ == "__main__":
    train_model()
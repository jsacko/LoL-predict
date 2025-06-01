import bentoml
from bentoml.io import JSON
import pandas as pd
from hydra import initialize, compose
from omegaconf import DictConfig
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "app")))
from app.features_builder import build_features_from_teamnames

initialize(config_path="configs", version_base="1.1")  # Initialize Hydra with the config path and version base
cfg: DictConfig = compose(config_name="config")
# Charger le modèle Bento
model_runner = bentoml.sklearn.get(f"{cfg["model"]["name"]}:latest").to_runner()

# Déclaration du service
svc = bentoml.Service("lol_predictor_service", runners=[model_runner])

# Déclaration de l'endpoint
@svc.api(input=JSON(), output=JSON())
def predict(input) -> dict:
    """Endpoint to predict the result of a match between two teams.
    This function takes the names of two teams and the path (optional) to their statistics
    Args:
        teamnameA (str): Name of team A.
        teamnameB (str): Name of team B.
        bo_type (str): Type of match (default is "1" for best of 1).
        
    Returns:
        dict: A dictionary containing the predicted winner and confidence level, or an error message if the prediction fails.
    """
    # Exemple d'extraction et feature engineering
    teamA = input.get("teamnameA")
    teamB = input.get("teamnameB")
    bo_type= input.get("bo_type", "1")
    if not teamA or not teamB:
        return {"error": "Both team names must be provided"}

    
    features_df = build_features_from_teamnames(cfg, teamA, teamB, bo_type)

    if features_df.empty:
        return {"error": "Invalid team names or missing data"}

    # Envoi au runner
    prediction = model_runner.predict.run(features_df)
    proba = model_runner.predict_proba.run(features_df)

    winner = teamA if prediction[0] == 1 else teamB
    confidence = round(float(proba[0][1] if prediction[0] == 1 else proba[0][0]),2)

    return {"winner": winner, "confidence": confidence}
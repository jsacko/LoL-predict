from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from app.model_loader import load_model
from app.features_builder import build_features_from_teamnames
from hydra import initialize, compose
from omegaconf import DictConfig

initialize(config_path="../configs") 
cfg: DictConfig = compose(config_name="config")
app = FastAPI()

model = load_model(cfg)
@app.post("/predict")
# Endpoint to predict the result of a match between two teams
def predict(teamnameA: str, teamnameB: str, bo_type: str = "1") -> dict:
    """Endpoint to predict the result of a match between two teams.
    This function takes the names of two teams and the path (optional) to their statistics
    Args:
        teamnameA (str): Name of team A.
        teamnameB (str): Name of team B.
        bo_type (str): Type of match (default is "1" for best of 1).
        
    Returns:
        dict: A dictionary containing the predicted winner and confidence level, or an error message if the prediction fails.
    """

    
    # Convertir l’objet Pydantic en DataFrame
    try:
        X = build_features_from_teamnames(cfg, teamnameA, teamnameB, bo_type)
        if X.empty:
            return {"error": "One of the teams is not found in the teams stats. Please check the team names."}
        # Prédiction
        prediction = model.predict(X)
        if prediction[0] == 1:
            return {"winner": teamnameA, "confidence": f"{float(model.predict_proba(X)[0][1]):.2f}"}
        elif prediction[0] == 0:
            return {"winner": teamnameB, "confidence": f"{float(model.predict_proba(X)[0][0]):.2f}"}
        else:
            return {"error": "Prediction not recognized. Please check the input data."}
    except Exception as e: # Return error 404 if an error occurs
        return {"error": str(e)}
# Update the database with the latest model predictions.
import mlflow.sklearn
import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import accuracy_score
import hydra
from omegaconf import DictConfig
import logging
import mlflow
import mlflow.sklearn
from src.utils.helpers import get_supabase_client
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def predict_and_send_to_supabase(cfg, X, y_validation=None):
    """
    Predict outcome and send to supabase
    """
    
    cols_features = list(cfg["data"]["features"])
    cols_website = list(cfg["data"]["cols_website"])
    if "result" not in X.columns.tolist():
        cols_website.remove("result")
    if "bo_id" not in X.columns.tolist():
        cols_website.remove("bo_id")
    model = joblib.load(cfg["model"]["output_path"])
    y_pred = model.predict(X)
    if y_validation is not None:
        accuracy = accuracy_score(y_validation, y_pred)
        mlflow.log_metric("accuracy", accuracy) # type: ignore
    y_pred_proba = model.predict_proba(X)
    df_predictions_actual_season = pd.DataFrame({"prediction":y_pred, "prediction_proba":y_pred_proba[:,1]})
    df_supabase = pd.concat([X[cols_features + cols_website].reset_index(drop=True), df_predictions_actual_season], axis=1)
    df_supabase = df_supabase.rename(columns={
        "teamnameA": "teamname_a",
        "teamnameB": "teamname_b",
    })
    supabase = get_supabase_client()
    # Replace such that all invalid values (NaN, inf) become Python native None (optional)
    df_supabase = df_supabase.replace([np.nan, np.inf, -np.inf], None)
    # Create base ID without counter (date only YYYY-MM-DD)
    df_supabase['base_id'] = df_supabase.apply(lambda x: f"{pd.to_datetime(x.date).strftime('%Y-%m-%d')}-{x.teamname_a}-{x.teamname_b}", axis=1)
    # Add counter to create final bo_id (1-based index)
    df_supabase['bo_id'] = (df_supabase.groupby('base_id').cumcount() + 1).astype(str) + '-' + df_supabase['base_id']
    df_supabase = df_supabase.drop(columns=['base_id'])
    df_supabase.date = df_supabase.date.astype("string")
    # Now convert to list of dicts while skipping None values per row
    data_to_insert = [
        {k: v for k, v in row.items() if v is not None}
        for row in df_supabase.to_dict(orient="records")
    ]
    
    df_supabase.prediction = df_supabase.prediction.astype(int)
    
    # Log the data we're about to send
    print("\nData to be upserted to Supabase:")
    print(df_supabase[['bo_id', 'date', 'teamname_a', 'teamname_b', 'prediction']].head())
    
    try:
        # Try to upsert the data
        response = supabase.table("matches").upsert(data_to_insert).execute()
        print("\nSuccessfully upserted data to Supabase!")
        print(f"Upserted {len(data_to_insert)} rows")
        return df_supabase
    except Exception as e:
        print("\nError upserting to Supabase:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error details: {str(e)}")
        
        # Try to get more details if available
        if hasattr(e, 'args') and e.args:
            print("\nAdditional error details:")
            print(e.args)
            
        # Print problematic data if any
        print("\nFirst few rows of problematic data:")
        print(data_to_insert[:2])  # Print first 2 rows for inspection
        
        return None


@hydra.main(config_path="../../configs", config_name="config", version_base="1.3") # type: ignore
def update_database(cfg: DictConfig):
    """
    Main function to evaluate the model.
    """
    project_root = hydra.utils.get_original_cwd()
    X = pd.read_csv(f"{cfg['paths']['processed_x']}")
    X_next_days = pd.read_csv(f"{cfg['paths']['processed_x_next_days']}")
    
    X_saved_train = pd.read_csv(f"{cfg['paths']['saved_training_data']}")
    X_validation = X[~X.date.isin(X_saved_train.date)]
    y_validation = X_validation.result

    logging.info(f"Prediction on season 2025 and next days. Model {cfg['model']['name']} with {len(X_validation)} games this season and {len(X_next_days)} next days games")
    mlflow.set_tracking_uri(cfg["tracking"]["mlflow_uri"])
    mlflow.set_experiment(cfg["tracking"]["daily_predictions"])
    with mlflow.start_run():
        mlflow.log_param("model_name", cfg["model"]["name"])
        mlflow.log_param("Number of games this season", len(X_validation))
        mlflow.log_param("Most recent game", X_validation.date.max())
        mlflow.log_param("Number of games next days", len(X_next_days))
        mlflow.log_param("Next days start date", X_next_days.date.min())
        model = joblib.load(cfg["model"]["output_path"])
        mlflow.sklearn.log_model(model, "model") # type: ignore

        mlflow.log_param("features", list(cfg["data"]["features"]))
        # Predict and send to Supabase
        print("\nProcessing validation data...")
        df_latest_prediction = predict_and_send_to_supabase(cfg, X_validation, y_validation)
        
        print("\nProcessing next days data...")
        df_next_days_prediction = predict_and_send_to_supabase(cfg, X_next_days)
        df_next_days_prediction.to_csv(f"{project_root}/{cfg['paths']['next_days_prediction']}", index=False)
        
        if df_latest_prediction is not None and df_next_days_prediction is not None:
            print("\n✅ Successfully updated all data in Supabase!")
        else:
            print("\n❌ There were issues updating some data in Supabase. Check the logs above for details.")
            
        logging.info("Prediction and upload to supabase completed successfully.")

if __name__ == "__main__":
    update_database()
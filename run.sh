#!/bin/bash

# Démarrer MLflow
mlflow server \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root ./artifacts \
    --host 0.0.0.0 \
    --port 5000 &

sleep 10  # attendre que le serveur MLflow démarre

# Exécuter l'entraînement
echo "Running pipeline..."
python src/pipelines/pipeline.py

# Terminer proprement

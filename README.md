# LoL-predict
A repository featuring a notebook that builds an AI using scikit-learn to predict the outcome of League of Legends games, along with a website where users can vote and compete against the AI.4

# Instructions utilisateur

## 1. Entraîner et sauvegarder le modèle dans le store local BentoML
python train_model.py

## 2. Builder le service Bento
bentoml build

## 3. Créer l’image Docker
bentoml containerize lol_predictor_service:latest

## 4. Lancer la stack
docker-compose up -d

# Tools
- [x] Scikit-learn
- [X] Separate the code of the notebook into module folder
    - [X] Data processing
    - [X] Feature engineering
    - [X] Model training
    - [X] Evaluation
- [X] Configuration file to keep experiments reproductible
- [] Pipeline tool Prefect
- [X] Containerizing models with Docker
- [X] Creating APIs with fast API or Flask, framework Bentoml to simplify the process
- [] Monitoring : Logging and dashboard with Graphana 
- [X] Versionning dataset and model :
    - [X] DVC 
    - [X] ML Flow
- [] Workflow with Airflow or Prefect
- [] Website


Model packaged in a docker container and deployed as a micro service (Docker)
Offer batch prediction to update recommendations nigthly (Prefect)
Real time API for ondemand predictions
Monitor for feature distribution shifts
Shadow deployments or circuit breakers so if my ML service fails, the system can revert to simpler strategies (à faire)

# Level 4 
- [] AWS Sagemaker, Vertex AI or Azure ML (Faire au retour)
- [] Orchestration with Kurbenetes (Faire au retour)
- [] Workflow tools like Airflow or Prefect (Faire au retour )
- [] Pytorch or TensorFlow for custom model development (2nd projet)
- [] Optimization methods like quantization, knowledge distribution
- [X] Experiment tracking and hyperparameter tuning with Weights and Biases or MLflow
- [] RAG, prompt tuning, incontext learning, MoE models (Au Travail et Shoot / 2nd projet)
- [] Distributed training across GPUs

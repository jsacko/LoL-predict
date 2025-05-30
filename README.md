# LoL-predict
A repository featuring a notebook that builds an AI using scikit-learn to predict the outcome of League of Legends games, along with a website where users can vote and compete against the AI.

# Tools
- [x] Scikit-learn
- [ ] Separate the code of the notebook into module folder
    - [] Data processing
    - [] Feature engineering
    - [] Model training
    - [] Evaluation
- [] Configuration file to keep experiments reproductible
- [] Pipeline tool Prefect
- [] Containerizing models with Docker
- [] Creating APIs with fast API or Flash, framework Bentoml to simplify the process
- [] Monitoring : Logging and dashboard with Graphana 
- [] Versionning dataset and model :
    - [] DVC 
    - [] ML Flow
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
- [] Workflow tools like Airflow or Prefect
- [] Pytorch or TensorFlow for custom model development
- [] Optimization methods like quantization, knowledge distribution
- [] Experiment tracking and hyperparameter tuning with Weights and Biases or MLflow
- [] RAG, prompt tuning, incontext learning, MoE models
- [] Distributed training across GPUs

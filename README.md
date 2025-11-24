# Cloud Azure End-to-End MLOps Pipeline - League of Legends Match Outcome Prediction 

[![Azure ML](https://img.shields.io/badge/Azure_ML-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com/en-us/services/machine-learning/)
[![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Apache Airflow](https://img.shields.io/badge/Apache_Airflow-0172E3?style=for-the-badge&logo=apache-airflow&logoColor=white)](https://airflow.apache.org/)
[![MLflow](https://img.shields.io/badge/MLflow-009A67?style=for-the-badge&logo=mlflow&logoColor=white)](https://mlflow.org/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/stable/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Numpy](https://img.shields.io/badge/Numpy-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
![SQL](https://img.shields.io/badge/SQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)

This project is a complete MLOps pipeline that predicts the outcome of **League of Legends esports matches**, spanning data ingestion, cloud-native training pipelines, and automated deployment. Designed for **production-level scalability on Microsoft Azure**, it simulates a real-world enterprise machine learning workflow.

---

## 🔍 Project Overview

The system automatically train, evaluate, and serve a predictive model that forecasts the winner of a LoL match given two competing teams. The system runs daily, updates with new data, makes predictions, and stores results in a live database.

The model reaches **67% accuracy**, delivering both real-time predictions and daily batch forecasts, and is deployed through a live web platform where users can compete against the AI by submitting their own predictions.

This project reflects a solid blend of data science, **MLOps**, and **full-stack engineering**, emphasizing **automation**, **scalability**, and **user interactio**, just like in a real-world tech environment.

### ✅ Key Features
  
- ☁️ **Azure ML Pipelines:** Core training and evaluation logic encapsulated in reproducible cloud pipelines.
- 🔄 **End-to-End ETL** + Feature Engineering: extracted raw match and team statistics, cleaned and transformed data into meaningful features for modeling
- 🎯 **Model Training & Experiment Tracking** with XGBoost, Hydra, MLflow, Weight & Biases
- ✅ **Pipeline Versioning & Reproducibility** with DVC
- 🌐 **API Deployment** with FastAPI and BentoML as a Dockerized microservice
- ⏱️ **Airflow to orchestrates** daily batch predictions into a Supabase-hosted **PostegreSQL** database
- 📊 **Monitoring** with Grafana + Prometheus: latency, failure rate, traffic
- 💻 **Frontend App** to interactively deliver predictions and compete against the AI
---

## ☁️ Deployment

The prediction engine utilizes a cloud-native architecture on **Microsoft Azure Machine Learning**. This setup moves heavy computation from local execution to a managed MLOps environment, ensuring scalability, version control, and automated retraining capabilities.

### Azure ML Training Pipeline
The model lifecycle is defined as a directed acyclic graph (DAG) within Azure Designer. This pipeline handles:
1.  **Data Ingestion:** Retrieval of historical match data.
2.  **Preprocessing:** Splitting data for training and validation to prevent leakage.
3.  **Modeling:** Training a **Two-Class Boosted Decision Tree**, optimized for tabular game data.
4.  **Evaluation:** Automated scoring to track model drift.
   
<img width="805" height="716" alt="Capture d&#39;écran 2025-08-28 011727" src="https://github.com/user-attachments/assets/2c106dba-614a-4a15-afe6-91e32c6897d7" />

### Production Integration
The trained model is deployed as an inference endpoint which consumes real-time match data and serves predictions to the frontend application.

* **Live Predictions:** The AI analyzes team compositions and historical stats to generate win probabilities for upcoming matches.
* **Performance Tracking:** A live leaderboard tracks the model's performance against human users.

| **Live Prediction Interface** | **Accuracy Leaderboard** |
|:---:|:---:|
|<img width="1128" height="752" alt="Capture d&#39;écran 2025-08-03 193550" src="https://github.com/user-attachments/assets/9e3e204d-dfdf-48c4-8ca9-69a462c55f38" />| <img width="553" height="581" alt="Capture d&#39;écran 2025-08-03 193618" src="https://github.com/user-attachments/assets/2f5e0418-06ca-489d-bbdf-43f914827364" /> |

## 🧱 Architecture

```text
      ┌───────────────────────────────────┐
      │   Historical Data & new matches   │
      └───────────────┬───────────────────┘
                      ▼
             ┌─────────────────────┐
             │ make_dataset.py     │  ← Clean & structure data
             └────────┬────────────┘
                      ▼
             ┌─────────────────────┐
             │ build_features.py   │  ← Feature engineering
             └────────┬────────────┘
                      ▼
             ┌─────────────────────┐
             │ train_model.py      │  ← Train + log model (MLflow)
             └────────┬────────────┘
                      ▼
             ┌─────────────────────┐
             │ evaluate_model.py   │  ← Evaluate & log metrics
             └────────┬────────────┘
                      ▼
             ┌───────────────────┐
             │ daily_predict.py  │ ← Predict results of upcoming matches daily
             └────────┬──────────┘
                      ▼
             ┌─────────────────────┐
             │ Supabase Database   │ ← Store predictions
             └────────┬────────────┘
                      ▼
             ┌─────────────────────────┐
             │ Leaderboard refreshed   │ ← Cron in SQL
             └─────────────────────────┘


  BentoML or Flask API Server   →   Serve predictions for chosen teams (live)
  Web App   →   Interface to compete against the AI by submitting your own predictions

````

---

## ⚙️ Technologies Used

| Category              | Tools & Frameworks                                                                 |
|-----------------------|-------------------------------------------------------------------------------------|
| **Cloud Infrastructure**   | Microsoft Azure Machine Learning · AWS S3 · Supabase (PostgreSQL)             |
| **Languages**         | Python · JavaScript                                                                |
| **ML & Data Science** | Scikit-learn · Numpy · Pandas · Seaborn                                            |
| **Experiment Tracking** | MLflow · Weight and Biases (W&B)                                                 |
| **MLOps & Orchestration** | Azure Pipelines · Apache Airflow · BentoML · DVC · Hydra · Git                 |
| **API & Deployment**  | FastAPI · Docker · BentoML                                                         |
| **Monitoring & Logging** | Grafana · Prometheus                                                            |
| **Frontend**          | Next.js · React                                                                    |


I integrated both FastAPI and BentoML into the project to gain hands-on experience with each. Moving forward, I would rely solely on BentoML, as it simplifies the deployment process by packaging both the API and the Docker container in one streamlined workflow.

For experiment tracking, I tested both MLflow and Weights & Biases, two leading tools in the MLOps ecosystem. Both are straightforward to set up, but since using both simultaneously is redundant, I decided to stick with MLflow, primarily because I preferred its user interface. The code related to Weights & Biases has been commented out for clarity.


---

## 🚀 How to Run Locally

1. **Clone the repo**:

   ```bash
   git clone https://github.com/your-username/lol-predict-mlops.git
   cd lol-predict-mlops
   ```

2. **Build the API and pipeline Docker image**:

   ```bash
   bentoml build
   bentoml containerize lol_predictor_service:latest
   ```
   Replace at the line 5 of docker-compose.yml with the new tag you obtained (e.g image: lol_predictor_service:j4233jlj4wdxf2h3)
   ```bash
   docker build -t lol-predict-ml-pipeline .
   ```

3. **Start Airflow, MLflow and all the service associated via Docker Compose**:

   ```bash
   docker-compose up --build
   ```

4. **Access services**:

   * Airflow UI: [http://localhost:8080](http://localhost:8080)
   * MLflow UI: [http://localhost:5000](http://localhost:5000)
   * Web App: [http://localhost:3000](http://localhost:3000)
   * Grafana : [http://localhost:3001](http://localhost:3001)
   * Prometheus : [http://localhost:9090](http://localhost:9090)

---

## 🌐 API Endpoint (Real-time Prediction)

Once the API is running:

```http
POST /predict
{
  "teamnameA": "G2 Esports",
  "teamnameB": "Fnatic"
}
```

Response:

```json
{
  "winner": "G2 Esports",
  "probability": 0.72
}
```

---

## 📅 Automation

* Airflow runs the full DAG every day at **2 AM UTC**.
* `make_dataset`, `build_features`, `train_model`, `evaluate_model` and `daily_predict.py` run in **DockerOperator** containers.
* `daily_predict.py` makes predictions and stores results in **Supabase**.
* You MUST use your own supabase database and set your api key and database url in a .env file at the root of the project to run `daily_predict.py`.
* You can create yours here : https://supabase.com/ 

---

## 📌 Project Status

✅ **Production Ready:** Full pipeline deployed on Azure ML.
✅ **Live Interface:** Web application connected to inference endpoints.
✅ **Automated:** Daily data ingestion triggers via Airflow.

**View the live deployment:** [lol-predictions-kappa.vercel.app](https://lol-predictions-kappa.vercel.app/)

---

## 👨‍💻 Author

**Julien SACKO** | Machine Learning Engineer 

[LinkedIn](https://www.linkedin.com/in/julien-sacko/)

---

## ⭐️ Show Your Support

If you find this project helpful, feel free to ⭐️ the repo and connect with me on LinkedIn!

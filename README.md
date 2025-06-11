# End-to-End MLOps Pipeline - League of Legends Match Outcome Prediction 

This project is a complete MLOps pipeline that predicts the outcome of **League of Legends esports matches**, from data collection to automated predictions and deployment. Designed for **production-level automation**, it simulates real-world workflows for machine learning systems.

---

## 🔍 Project Overview

The goal is to automatically train, evaluate, and serve a predictive model that forecasts the winner of a LoL match given two competing teams. The system runs daily, updates with new data, makes predictions, and stores results in a live database.

The model reaches **67% accuracy**, delivering both real-time predictions and daily batch forecasts, and is deployed through a live web platform where users can compete against the AI by submitting their own predictions.

This project reflects a solid blend of data science, **MLOps**, and **full-stack engineering**, emphasizing **automation**, **scalability**, and **user interactio**n—just like in a real-world tech environment.

### ✅ Key Features
  
- 🔄 **End-to-End ETL** + Feature Engineering: extracted raw match and team statistics, cleaned and transformed data into meaningful features for modeling
- 🎯 **Model Training & Experiment Tracking** with XGBoost, Hydra, MLflow, Weight & Biases
- ✅ **Pipeline Versioning & Reproducibility** with DVC
- 🌐 **API Deployment** with FastAPI and BentoML as a Dockerized microservice
- ⏱️ **Airflow to orchestrates** daily batch predictions into a Supabase-hosted **PostegreSQL** database
- 📊 **Monitoring** with Grafana + Prometheus: latency, failure rate, traffic
- ☁️ **Cloud-ready architecture** (compatible with GCP Cloud Run / AWS SageMaker)
- 💻 **Frontend App** to interactively deliver predictions and compete against the AI
---

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
             ┌────────────────────────────┐
             │ daily_predict.py (Airflow) │ ← Predict new matches daily
             └────────┬───────────────────┘
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
| **Languages**         | Python · JavaScript                                                                |
| **ML & Data Science** | Scikit-learn · Numpy · Pandas · Seaborn                                            |
| **Experiment Tracking** | MLflow · Weight and Biases (W&B)                                                 |
| **MLOps & Orchestration** | Apache Airflow · BentoML · DVC · Hydra · Git                                  |
| **API & Deployment**  | FastAPI · Docker · BentoML                                                         |
| **Monitoring & Logging** | Grafana · Prometheus                                                            |
| **Cloud & Storage**   | AWS S3 · PostgreSQL (Supabase)                                                                           |
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

2. **Build the Docker pipeline image**:

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
   * Grafana : [http://localhost:3001](http://localhost:3001)
   * Prometheus : [http://localhost:9090](http://localhost:9090)
   * BentoML API: [http://localhost:3000](http://localhost:3000) (if launched)

---

## 🌐 API Endpoint (Real-time Prediction)

Once the API is running:

```http
POST /predict
{
  "teamname_a": "G2 Esports",
  "teamname_b": "Fnatic"
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

## 📝 Future Improvements

* Add **Model Drift Detection**
* Improve frontend of the web application

---

## 📌 Project Status


✅ MVP complete with full automation

🚀 Deployed locally with Docker

🧪 Cloud-ready with AWS (ECR + ECS)

🔧 The website is deployed ! 
https://lol-predictions-kappa.vercel.app/

---

## 👨‍💻 Author

**Julien SACKO** | Machine Learning Engineer 

[LinkedIn](https://www.linkedin.com/in/julien-sacko/) · [GitHub](https://github.com/jsacko)

---

## ⭐️ Show Your Support

If you find this project helpful, feel free to ⭐️ the repo and connect with me on LinkedIn!

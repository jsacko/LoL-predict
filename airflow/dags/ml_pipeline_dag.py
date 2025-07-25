from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.python import PythonOperator
from pathlib import Path
from datetime import datetime, timedelta
from docker.types import Mount
import subprocess
import os
from dotenv import load_dotenv
load_dotenv()

data_path = Path(__file__).resolve().parent.parent


default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def run_script(script_path):
    subprocess.run(["python", script_path], check=True)

with DAG(
    dag_id="ml_pipeline_dag",
    default_args=default_args,
    start_date=datetime(2025, 5, 3),
    schedule="0 2 * * *",  # tous les jours à 2h
    catchup=False,

) as dag:

    make_dataset = DockerOperator(
        task_id="make_dataset",
        image="lol-predict-lol-predict-ml-pipeline:latest", 
        command="python src/data/make_dataset.py",
        docker_url="unix://var/run/docker.sock",
        mounts= [Mount(source="lol-predict-airflow-storage", target="/app/data/processed", type="volume")], # Store processed data in a Docker volume
        mount_tmp_dir=False,  #
        auto_remove="success",    
    )

    build_features = DockerOperator(
        task_id="build_features",
        image="lol-predict-lol-predict-ml-pipeline:latest", 
        command="python src/features/build_features.py",
        docker_url="unix://var/run/docker.sock",
        mounts= [Mount(source="lol-predict-airflow-storage", target="/app/data/processed", type="volume")], # Use processed data from the Docker volume
        mount_tmp_dir=False, 
        auto_remove="success",
    )

    train_model = DockerOperator(
        task_id="train_model",
        image="lol-predict-lol-predict-ml-pipeline:latest", 
        command="python src/models/train_model.py",
        docker_url="unix://var/run/docker.sock",
        mounts= [Mount(source="lol-predict-airflow-storage", target="/app/models", type="volume")], # Store trained models in a Docker volume
        network_mode="lol-predict_airflow_network", # Access to mlflow server
        auto_remove="success",
    )

    evaluate_model = DockerOperator(
        task_id="evaluate_model",
        image="lol-predict-lol-predict-ml-pipeline:latest", #
        command="python src/models/evaluate_model.py",
        docker_url="unix://var/run/docker.sock",
        mounts= [Mount(source="lol-predict-airflow-storage", target="/app/models", type="volume")], # Use trained models from the Docker volume
        network_mode="lol-predict_airflow_network", # Access to mlflow server
        auto_remove="success",    
    )

    daily_update = DockerOperator(
        task_id="daily_update",
        image="lol-predict-lol-predict-ml-pipeline:latest", 
        command="python src/models/daily_update.py",
        docker_url="unix://var/run/docker.sock",
        environment={
        'SUPABASE_KEY': '{{ var.value.SUPABASE_KEY }}',
        'SUPABASE_URL': '{{ var.value.SUPABASE_URL }}',
        },
        mounts=[
        Mount(source="lol-predict-airflow-storage", target="/app/data/processed", type="volume"),
        Mount(source="lol-predict-airflow-storage", target="/app/models", type="volume"),
        ],
        network_mode="lol-predict_airflow_network", # Access to mlflow server
        auto_remove="success",    
    )

    make_dataset >> build_features >> train_model >> evaluate_model >> daily_update

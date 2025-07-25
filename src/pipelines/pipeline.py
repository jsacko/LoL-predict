import subprocess
import sys
import hydra
from omegaconf import DictConfig
from pathlib import Path


@hydra.main(config_path="../../configs", config_name="config", version_base="1.3") # type: ignore

def run_pipeline(cfg: DictConfig):
    python_path = Path(sys.executable)  # récupère le chemin du Python actif (dans .venv)
    subprocess.run([str(python_path), f"{cfg['paths']['daily_update.py']}"], check=True)
    subprocess.run([str(python_path), f"{cfg['paths']['make_dataset.py']}"], check=True)
    subprocess.run([str(python_path), f"{cfg['paths']['build_features.py']}"], check=True)
    subprocess.run([str(python_path), f"{cfg['paths']['train_model.py']}"], check=True)
    subprocess.run([str(python_path), f"{cfg['paths']['evaluate_model.py']}"], check=True)
    

if __name__ == "__main__":
    run_pipeline()

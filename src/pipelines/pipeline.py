import subprocess
import hydra
from omegaconf import DictConfig

@hydra.main(config_path="../../configs", config_name="config", version_base="1.3") # type: ignore

def run_pipeline(cfg: DictConfig):
    subprocess.run(["python", f"{cfg["paths"]["make_dataset.py"]}"], check=True)
    subprocess.run(["python", f"{cfg["paths"]["build_features.py"]}"], check=True)
    subprocess.run(["python", f"{cfg["paths"]["train_model.py"]}"], check=True)
    subprocess.run(["python", f"{cfg["paths"]["evaluate_model.py"]}"], check=True)

if __name__ == "__main__":
    run_pipeline()

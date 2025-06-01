import joblib
import hydra
import logging
from omegaconf import DictConfig

def load_model(cfg):
    """
    Load a pre-trained model from the specified path in config.
    Args:
        cfg (DictConfig): Configuration object containing model path.
    Returns:
        The loaded model.
    """
    # Load the model using joblib
    model_path = cfg["model"]["output_path"]
    if joblib.os.path.exists(model_path):
        logging.info(f"Loading the model found at {model_path}")
        model = joblib.load(model_path)
        return model
    else:
        raise FileNotFoundError(f"Model file not found at {model_path}. Please check the path in the configuration.")
    
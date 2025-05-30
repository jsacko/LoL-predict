import pandas as pd
import glob
import os
import gdown
import logging
import hydra
from omegaconf import DictConfig
 


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_csvs_from_folder(folder_path: str, pattern="*.csv") -> pd.DataFrame:
    files = glob.glob(os.path.join(folder_path, pattern))
    logging.info(f"Found {len(files)} files")
    return pd.concat([pd.read_csv(f, index_col="gameid", parse_dates=True) for f in files])

def download_latest_data(url: str, output_path: str):
    """
    Downloads the latest data from the given URL and saves it to the specified output path.
    """
    
    gdown.download(url, output_path, quiet=False)
    logging.info(f"Downloaded latest data to {output_path}")


@hydra.main(config_path="../../configs", config_name="config", version_base="1.3") # type: ignore
def main(cfg: DictConfig):
    raw_data_dir = f"{cfg["data"]["raw_data_dir"]}"
    output_file = f"{cfg["data"]["merged_output_file"]}"
    output_path_latest_data = f"{cfg['data']['download_output_path']}"
    download_url_latest_data = cfg["data"]["download_url"]
    
    
    logging.info(f"output file {output_file}")
    if os.path.exists(output_file):
        logging.info("Merged file already exists. Loading cached version.")
        df_all = pd.read_csv(output_file, index_col="gameid", parse_dates=True)
    else:
        logging.info("Merging all CSVs in raw data directory...")
        df_all = load_csvs_from_folder(raw_data_dir)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df_all.to_csv(output_file)
        logging.info(f"Saved merged dataset to {output_file}")

    logging.info(f"Preview of merged dataset:\n{df_all.head()}")

    download_latest_data(download_url_latest_data, output_path_latest_data)
    if os.path.exists(output_path_latest_data):
        logging.info(f"Latest data downloaded to {output_path_latest_data}")
    else:
        logging.error(f"Failed to download latest data to {output_path_latest_data}")
    


if __name__ == "__main__":
    main()
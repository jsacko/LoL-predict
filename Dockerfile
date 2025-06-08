FROM python:3.10

WORKDIR app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./src ./src
COPY ./configs ./configs

RUN mkdir -p data/raw data/processed

COPY ./data/raw/2024_LoL_esports_match_data_from_OraclesElixir.csv ./data/raw/2024_LoL_esports_match_data_from_OraclesElixir.csv
COPY ./data/raw/2023_LoL_esports_match_data_from_OraclesElixir.csv ./data/raw/2023_LoL_esports_match_data_from_OraclesElixir.csv
COPY ./data/raw/2022_LoL_esports_match_data_from_OraclesElixir.csv ./data/raw/2022_LoL_esports_match_data_from_OraclesElixir.csv
COPY ./data/raw/2021_LoL_esports_match_data_from_OraclesElixir.csv ./data/raw/2021_LoL_esports_match_data_from_OraclesElixir.csv
COPY ./data/raw/2020_LoL_esports_match_data_from_OraclesElixir.csv ./data/raw/2020_LoL_esports_match_data_from_OraclesElixir.csv
COPY ./data/processed/saved_training_data.csv ./data/processed/saved_training_data.csv
COPY ./data/processed/X.csv ./data/processed/X.csv
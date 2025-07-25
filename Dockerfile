FROM python:3.10

WORKDIR app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./src ./src
COPY ./configs ./configs

RUN mkdir -p data/raw data/processed

COPY ./data/processed/saved_training_data.csv ./data/processed/saved_training_data.csv

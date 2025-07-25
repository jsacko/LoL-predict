FROM python:3.10

WORKDIR app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./src ./src
COPY ./configs ./configs
COPY ./run.sh ./run.sh


RUN mkdir -p data/raw data/processed
RUN chmod +x run.sh


COPY ./data/processed/saved_training_data.csv ./data/processed/saved_training_data.csv

# Commande de démarrage
CMD ["./run.sh"]

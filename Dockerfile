# Dockerfile
FROM python:3.10

WORKDIR /app

COPY app ./app
COPY models ./configs
COPY configs ./configs
COPY data/processed/teams_stats.csv ./data/processed/teams_stats.csv
COPY bento_service.py .

RUN pip install --upgrade pip
# BentoML CLI pour le service
RUN pip install bentoml prometheus_client hydra-core omegaconf scikit-learn pandas numpy scikit-learn joblib

EXPOSE 3000
EXPOSE 8001

CMD ["bentoml", "serve", "./bento_service.py"]
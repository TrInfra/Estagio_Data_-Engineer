# syntax=docker/dockerfile:1

FROM python:3.12.3-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

# Copia o código da aplicação para o diretório de trabalho
COPY . .

# Define o comando padrão a ser executado ao iniciar o contêiner
CMD ["python", "carguru.py"]
import os
import json
import boto3
import requests
from datetime import datetime
from typing import List, Dict

def buscar_filmes(url_api: str, headers: Dict[str, str]) -> List[Dict]:
    all_movies = []
    unique_ids = set()
    total_results = 8000
    current_page = 1

    while len(unique_ids) < total_results:
        url = f"{url_api}&page={current_page}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if 'results' in data:
            for movie in data['results']:
                if movie['id'] not in unique_ids:
                    all_movies.append(movie)
                    unique_ids.add(movie['id'])
        else:
            break

        if current_page >= data['total_pages']:
            break

        current_page += 1

    return all_movies[:total_results]

def criar_caminho_s3(categoria: str, nome_arquivo: str) -> str:
    process_date = datetime.now().strftime("%Y/%m/%d")
    year, month, day = process_date.split('/')
    return f"Raw/TMDB/JSON/{year}/{month}/{day}/{categoria}/{nome_arquivo}"

def enviar_arquivos_para_s3_acao(filmes_acao: List[Dict], bucket: str, client: boto3.client, itens_por_arquivo: int = 100):
    num_arquivos = (len(filmes_acao) + itens_por_arquivo - 1) // itens_por_arquivo
    for i in range(num_arquivos):
        inicio_idx = i * itens_por_arquivo
        fim_idx = min((i + 1) * itens_por_arquivo, len(filmes_acao))
        nome_arquivo = f"filmes_acao_{i + 1}.json"
        s3_path = criar_caminho_s3("Acao", nome_arquivo)

        filmes_chunk = filmes_acao[inicio_idx:fim_idx]
        filmes_chunk_json = json.dumps(filmes_chunk, ensure_ascii=False, indent=4)

        client.put_object(Body=filmes_chunk_json, Bucket=bucket, Key=s3_path)

def enviar_arquivos_para_s3_aventura(filmes_aventura: List[Dict], bucket: str, client: boto3.client, itens_por_arquivo: int = 100):
    num_arquivos = (len(filmes_aventura) + itens_por_arquivo - 1) // itens_por_arquivo
    for i in range(num_arquivos):
        inicio_idx = i * itens_por_arquivo
        fim_idx = min((i + 1) * itens_por_arquivo, len(filmes_aventura))
        nome_arquivo = f"filmes_aventura_{i + 1}.json"
        s3_path = criar_caminho_s3("Aventura", nome_arquivo)

        filmes_chunk = filmes_aventura[inicio_idx:fim_idx]
        filmes_chunk_json = json.dumps(filmes_chunk, ensure_ascii=False, indent=4)

        client.put_object(Body=filmes_chunk_json, Bucket=bucket, Key=s3_path)

def lambda_handler(event, context):
    with open('config.json') as config_file:
        config = json.load(config_file)

    aws_access_key_id = config['aws_access_key_id']
    aws_secret_access_key = config['aws_secret_access_key']
    aws_session_token = config['aws_session_token']
    tmdb_api_token = config['tmdb_api_token']
    bucket_name = config['bucket_name']

    client = boto3.client(
        service_name='s3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token
    )

    url_acao = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=pt-br&with_genres=28&sort_by=vote_average.desc&release_date.gte=1900-01-01&release_date.lte=2024-07-10&vote_count.gte=100"
    url_aventura = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=pt-br&with_genres=12&sort_by=popularity.desc&release_date.gte=1900-01-01&release_date.lte=2024-07-10&vote_count.gte=100"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {tmdb_api_token}"
    }

    filmes_acao = buscar_filmes(url_acao, headers)
    enviar_arquivos_para_s3_acao(filmes_acao, bucket_name, client, itens_por_arquivo=100)

    filmes_aventura = buscar_filmes(url_aventura, headers)
    enviar_arquivos_para_s3_aventura(filmes_aventura, bucket_name, client, itens_por_arquivo=100)

    return {
        'statusCode': 200,
        'body': json.dumps(f"Filmes armazenados")
         }
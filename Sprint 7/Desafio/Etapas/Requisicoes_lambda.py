import os
import json
import boto3
import requests
from datetime import datetime

def buscar_filmes(url, headers):
    all_movies = []
    unique_ids = set()
    total_results = 1000
    current_page = 1

    while len(unique_ids) < total_results:
        response = requests.get(url, headers=headers)
        data = response.json()

        if 'results' in data:
            for movie in data['results']:
                if movie['id'] not in unique_ids:
                    all_movies.append(movie)
                    unique_ids.add(movie['id'])
        else:
            break

        if data['page'] >= data['total_pages']:
            break

        current_page += 1
        url = f"{url.split('?')[0]}?page={current_page}"

    return all_movies[:total_results]

def create_s3_path(file_name):
    process_date = datetime.now().strftime("%Y/%m/%d")
    year, month, day = process_date.split('/')
    
    return f"Raw/TMDB/JSON/{year}/{month}/{day}/{file_name}"

def enviar_arquivos_para_s3(movies, bucket, client, itens_por_arq=100):
    num_arq = (len(movies) + itens_por_arq - 1) // itens_por_arq
    for i in range(num_arq):
        inicio_idx = i * itens_por_arq
        fim_idx = min((i + 1) * itens_por_arq, len(movies))
        file_name = f"filmes_acao_{i + 1}.json"
        s3_path = create_s3_path(file_name)

        movies_chunk = movies[inicio_idx:fim_idx]
        movies_chunk_json = json.dumps(movies_chunk, ensure_ascii=False, indent=4)

        client.put_object(Body=movies_chunk_json, Bucket=bucket, Key=s3_path)

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

    url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=pt-br&page=1&release_date.gte=2000-01-01&release_date.lte=2023-12-30&sort_by=vote_average.desc&vote_count.gte=100&with_genres=28"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {tmdb_api_token}"
    }

    movies = buscar_filmes(url, headers)
    enviar_arquivos_para_s3(movies, bucket_name, client)

    return {
        'statusCode': 200,
        'body': json.dumps(f"Número de filmes armazenados: {len(movies)}")
    }
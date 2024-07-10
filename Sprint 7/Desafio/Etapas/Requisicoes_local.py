import requests
import json
import os
import boto3
from datetime import datetime
from dotenv import load_dotenv
#============================================Funções====================================================
def buscar_path_arquivo(file_name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

def buscar_filmes(url,headers):
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

def salvar_arq_json(movies , file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)

def separar_filme_por_arquivo(movies, itens_por_arq):
    num_arq = (len(movies) + itens_por_arq - 1) // itens_por_arq
    for i in range(num_arq):
        inicio_idx = i * itens_por_arq
        fim_idx = min((i + 1) * itens_por_arq, len(movies))
        file_name = f"filmes_acao_{i + 1}.json"
        file_path = buscar_path_arquivo(f"arquivosjson/{file_name}")
        salvar_arq_json(movies[inicio_idx:fim_idx], file_path)

def create_s3_path(file_name):
    process_date = datetime.now().strftime("%Y/%m/%d")
    year, month, day = process_date.split('/')
    
    return f"Raw/TMDB/JSON/{year}/{month}/{day}/{file_name}"

def enviar_arquivos_para_s3(arquivos, bucket, client):
    for arquivo in arquivos:
        s3_path = create_s3_path(os.path.basename(arquivo))
        client.upload_file(arquivo, bucket, s3_path)

def listar_arquivos_diretorio(diretorio):
    arquivos = []
    for root, dirs, files in os.walk(diretorio):
        for file in files:
            if file.endswith(".json"):
                arquivos.append(os.path.join(root, file))
    return arquivos
#===========================================================================================================


#============================================Credenciais====================================================

load_dotenv()

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_session_token = os.getenv('AWS_SESSION_TOKEN')


client = boto3.client(
    service_name='s3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)
#===========================================================================================================

bucket_name = "data-lake-do-nycolas"

url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=pt-br&page=1&release_date.gte=2000-01-01&release_date.lte=2023-12-30&sort_by=vote_average.desc&vote_count.gte=100&with_genres=28"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3YzQ3YWI1MzNjZTNiNmU0YzAyOTAyNjA0ODE4YTM3OCIsIm5iZiI6MTcyMDYyNjQ3NC4yNjkwNDksInN1YiI6IjY2ODU4ODAxZmNiY2Q3NWU3ODNiMmI4MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.AMdEloM2NB0Ry2fFJHDfyI62lynTml6OM9b0Rz0hvMU"
    }


movies = buscar_filmes(url,headers)
separar_filme_por_arquivo(movies, itens_por_arq=100)

diretorio_arquivosjson = buscar_path_arquivo("arquivosjson/")
arquivos = listar_arquivos_diretorio(diretorio_arquivosjson)
enviar_arquivos_para_s3(arquivos, bucket_name, client)


print(f"Número de filmes armazenados: {len(movies)}")
print("Os dados foram salvos em filmes_acao.json")

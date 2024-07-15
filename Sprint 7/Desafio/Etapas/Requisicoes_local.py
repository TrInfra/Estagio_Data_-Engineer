import requests
import json
import os
import boto3
from datetime import datetime
from dotenv import load_dotenv

#============================================Funções====================================================
def buscar_path_arquivo(file_name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

def buscar_filmes(api_url, headers):
    all_movies = []
    unique_ids = set()
    total_results = 8000
    current_page = 1

    while len(unique_ids) < total_results:
        url = f"{api_url}&page={current_page}"
        response = requests.get(url, headers=headers)
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


def salvar_arq_json(movies, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)

def separar_filme_por_arquivo_acao(movies, itens_por_arq):
    num_arq = (len(movies) + itens_por_arq - 1) // itens_por_arq
    for i in range(num_arq):
        inicio_idx = i * itens_por_arq
        fim_idx = min((i + 1) * itens_por_arq, len(movies))
        file_name = f"filmes_acao_{i + 1}.json"
        file_path = buscar_path_arquivo(f"arquivosjson/Acao/{file_name}")
        salvar_arq_json(movies[inicio_idx:fim_idx], file_path)

def separar_filme_por_arquivo_aventura(movies, itens_por_arq):
    num_arq = (len(movies) + itens_por_arq - 1) // itens_por_arq
    for i in range(num_arq):
        inicio_idx = i * itens_por_arq
        fim_idx = min((i + 1) * itens_por_arq, len(movies))
        file_name = f"filmes_aventura_{i + 1}.json"
        file_path = buscar_path_arquivo(f"arquivosjson/Aventura/{file_name}")
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
tokenAPI = os.getenv('tokenAPI')
bucketname_s3 = os.getenv('bucket_name_s3')

client = boto3.client(
    service_name='s3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)
#===========================================================================================================

bucket_name = f"{bucketname_s3}"

url_acao = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=pt-br&with_genres=28&sort_by=popularity.desc&release_date.gte=1900-01-01&release_date.lte=2024-07-10&vote_count.gte=100"
url_aventura = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=pt-br&with_genres=12&sort_by=popularity.desc&release_date.gte=1900-01-01&release_date.lte=2024-07-10&vote_count.gte=100"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {tokenAPI}"
    }

movies_acao = buscar_filmes(url_acao, headers)
separar_filme_por_arquivo_acao(movies_acao, itens_por_arq=100)

movies_aventura = buscar_filmes(url_aventura, headers)
separar_filme_por_arquivo_aventura(movies_aventura, itens_por_arq=100)

diretorio_arquivosjson = buscar_path_arquivo("arquivosjson/")
arquivos = listar_arquivos_diretorio(diretorio_arquivosjson)
enviar_arquivos_para_s3(arquivos, bucket_name, client)

print(f"Número de filmes de ação armazenados: {len(movies_acao)}")
print(f"Número de filmes de aventura armazenados: {len(movies_aventura)}")
print("Os dados foram salvos em filmes_acao.json")
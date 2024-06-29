import boto3
import os
from datetime import datetime
from tqdm import tqdm
from dotenv import load_dotenv
import pandas as pd
# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Função para obter o caminho local do arquivo
def get_local_file_path(file_name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

# Função para criar o caminho no S3
def create_s3_path(data_type, file_name):
    process_date = datetime.now().strftime("%Y/%m/%d")
    year, month, day = process_date.split('/')
    
    return f"Raw/Local/CSV/{data_type.capitalize()}/{year}/{month}/{day}/{file_name}"

def create_bucket_if_not_exists(bucket_name, client):
    try:
        client.head_bucket(Bucket=bucket_name)
        print(f"O bucket '{bucket_name}' já existe.")
    except client.exceptions.NoSuchBucket:
        client.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' criado com sucesso.")
        
class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._tqdm = tqdm(total=self._size, unit='B', unit_scale=True, desc=filename, miniters=1)

    def __call__(self, bytes_amount):
        self._seen_so_far += bytes_amount
        self._tqdm.update(bytes_amount)
    
    def close(self):
        self._tqdm.close()

movies_csv = get_local_file_path("movies.csv")
series_csv = get_local_file_path("series.csv")

# Carregando credenciais AWS das variáveis de ambiente
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_session_token = os.getenv('AWS_SESSION_TOKEN')


if not aws_access_key_id or not aws_secret_access_key:
    raise EnvironmentError("Credenciais AWS não encontradas.")

client = boto3.client(
    service_name='s3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

bucket_name = "data-lake-do-nycolas"

# Verificar se o bucket existe e criar se não existir
create_bucket_if_not_exists(bucket_name, client)

# Verifica se os arquivos existem
if os.path.exists(movies_csv) and os.path.exists(series_csv):
    try:
        movies_df = pd.read_csv(movies_csv, delimiter='|')
        series_df = pd.read_csv(series_csv, delimiter='|')


        s3_path_movies = create_s3_path("Movies", "movies.csv")
        progress_movies = ProgressPercentage(movies_csv) # Barra de progresso para vizualizar
        client.upload_file(movies_csv, bucket_name, s3_path_movies.replace("\\", "/"), Callback=progress_movies)
        progress_movies.close()
        print()
        print(f"Arquivo movies_csv enviado com sucesso para o bucket '{bucket_name}'")
        print()
        print()

        s3_path_series = create_s3_path("Series", "series.csv")
        progress_series = ProgressPercentage(series_csv) # Barra de progresso para vizualizar
        client.upload_file(series_csv, bucket_name, s3_path_series.replace("\\", "/"), Callback=progress_series)
        progress_series.close()
        print()
        print(f"Arquivo series_csv enviado com sucesso para o bucket '{bucket_name}'")
        print()
        print()
    except Exception as e:
        print(f"Erro ao enviar os arquivos: {e}")
else:
    print("Um ou mais arquivos estão faltando. Upload não realizado.")

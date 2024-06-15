import boto3
import json
import os

# Diretório local do arquivo
local_arquivo = os.path.dirname(os.path.abspath(__file__))

# Configuração do cliente S3
client = boto3.client(
    's3',
    aws_access_key_id='ASIAYS2NQHGHSJ3WDN6O',
    aws_secret_access_key='nHvi+RQHsfraRc8JBz3bSrz0gGj82eh+kwlLfxu1',
    aws_session_token='IQoJb3JpZ2luX2VjECsaCXVzLWVhc3QtMSJHMEUCIAunLdsyyUXBei7+RFsdnxriKJdUQcAO5fdghLs6NSr9AiEA3jZ3OEjX7sIdVy38ebkQu7ouQJAjAyUIts9yH8lFDSMqsAMIxP//////////ARAAGgw1OTAxODM2NzYzMDMiDOERbcy74zE7V+Q6QSqEA1y23IrM+9aexDlFqS2Q6BvnDzkl7BILfG7j5KZ8mDtkAd5HnEQ2cYcWMaYsUAwdd6cj5rs/mZvFY5aAleAgUnI7m1nn2oUzbDHYq96jDHKT8BBErDy3ZJps6qmTQnbGRQjGo+B4Qgg+hmQQV+GDbtQWBPQeFIzUaCB9WJ/zcX6xBMvEY1HHq5huDrrghqSzGYe/PzT+eljtTpioWdcamFDa6cDu1swsgOxoX1lUv1HPM7s9NHNxDu7z8IY31DCIWZrRVblgegWmmppOYOyYlN/6Lgp60SYQNmTIWdnGde5Lbs4pWz+W9POc3o+9V/+gdV2TESc3nllxdAcAAgftKwFY9gF7Imf1l8ctTZ75eWT0YV21PPG9oD42CSvkkLYdMlVT6S6GPDycO+8Lejv06a7jQtBGCAPtS0tFKd79Tx8qXMeK2d92695KdwbwLBMFnuCW4k4+sctU4X65LgvGnyLf9j31nVbbDvyC+VIln7YNbtKU/XUwZJOdQ+2QFY36xXrJWLUw9cC3swY6pgFKu89dsCaconz/RNKai4sEKDN6eo85JQy4LjZ4HUyM06gM3KqN5Pu6GTEwf2AMAziaOjSd/wdL9fbllT/kT6xRExip1OYcAoBVjngfPwXAGAnC8BZS6FcJ5U5Q84BuyvwFLGluyl9hRQ3+Mhb1XB3SZby6k6oAuZ4uRw/bAgVEqYJ4p27ZUL+PdBUi+SE3HmRi+bz68+3pO0bzDIAZ/0t56MS340RL'
)
# Função para ler o conteúdo de um arquivo S3
def read_s3_file(bucket_name, file_key):
    obj = client.get_object(Bucket=bucket_name, Key=file_key)
    return obj['Body'].read().decode('utf-8')

# Define os parâmetros do bucket e dos arquivos
bucket_name = 'desafiosprint05nyck'
sql_file_key = 'Query.sql'
csv_file_key = 'V_OCORRENCIA_AMPLA_Cleaned.csv'

# Lê o conteúdo do arquivo SQL
query = read_s3_file(bucket_name, sql_file_key)
print(f"Query SQL: {query}")

# Configuração da entrada (CSV)
input_serialization = {
    'CSV': {
        'FileHeaderInfo': 'USE',  # Usei pois o csv tem cabeçalho
        'RecordDelimiter': '\n',  # Delimitador de linha
        'FieldDelimiter': ',',    # Delimitador de campo
        'QuoteCharacter': '"',   
        'AllowQuotedRecordDelimiter': True 
    }
}

# Configuração da saída (JSON)
output_serialization = {
    'JSON': {
        'RecordDelimiter': '\n'  
    }
}

# Executa a query SQL no arquivo CSV
try:
    response = client.select_object_content(
        Bucket=bucket_name,
        Key=csv_file_key,
        Expression=query,
        ExpressionType='SQL',
        InputSerialization=input_serialization,
        OutputSerialization=output_serialization,
        RequestProgress={'Enabled': True}  # Habilita a exibição de progresso
    )

    results = []
    # Processa a response
    for event in response['Payload']:
        if 'Records' in event:
            records = event['Records']['Payload']
            # Decodifica e adiciona o resultado à lista
            records_decoded = records.decode('utf-8').strip()
            if records_decoded:
                result = json.loads(records_decoded)  # Decodifica a string JSON para um objeto Python
                # Usei para formatar os numero adequadamente
                result_fixed = {
                    key: "{:.1f}".format(value) if isinstance(value, float) else value
                    for key, value in result.items()
                }
                results.append(result_fixed)

    # Escreve os resultados no arquivo JSON
    output_file_path = os.path.join(local_arquivo, "output.json")
    with open(output_file_path, "w") as arq_json:
        json.dump(results, arq_json, indent=4)  

    print(f"Resultados armazenados em {output_file_path}") # Para mostrar onde salvei o resultado do output

except Exception as e:
    print(f"Erro ao executar a consulta: {e}")
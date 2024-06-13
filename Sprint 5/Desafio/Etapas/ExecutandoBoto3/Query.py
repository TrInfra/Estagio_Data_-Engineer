import boto3
import json
import os

# Diretório local do arquivo
local_arquivo = os.path.dirname(os.path.abspath(__file__))

# Configuração do cliente S3
client = boto3.client(
    's3',
    aws_access_key_id='ASIAYS2NQHGHYDEWHZPT',
    aws_secret_access_key='ycgiBYrsWDU2O2CHPtKVUr3N9+kNlfWCVbchsVoS',
    aws_session_token='IQoJb3JpZ2luX2VjEOP//////////wEaCXVzLWVhc3QtMSJIMEYCIQCMd9Gm10bApNIk9vr85g5AGyLcBK/d8sR0V4bU3Zrr/QIhAJRiHYSH5JY6UIuuJjaZai5nNQS159obJxuzq7bb1M8pKqcDCHwQABoMNTkwMTgzNjc2MzAzIgyCRNuvi+upiGjGv4oqhAPFB4F39P1Rbne3q56NR6fEM4i2GhZBWUAdkFlI6hrmLrbseLBwr8GmKzJk+f6+rfTJNpifNgvXhuhueS21CgLWhmGlCz38J3QCgswKQMaeGI59yO2CPtWGkpUIV1CCdl5lpGkpczP8xBoX25kIooctREiLYNyCtZRxmAK7n8gpW4FjrsdD4KMvnEu0EuP4o1T0yRgMGxPyL5W3R8iuc9iBHsR8Ume+jWeckGKGQg0NKdss6BD3Qgv1x7Z7sw3E5Eb2MywJWox0ptwjHT9CUWtRTXA8Oi2RspuGhjeWIt1B4Pd8aswq4FqTNujgwqxZiTF7E+UjM9IBJnTTS8ojZfnfWkYyMH+RKffFlO4bS0l5CkxWbMmgkyRIZij0AY19dx2Vp4UvHPNEuBJMuuozoCa5pGZSxNs5JcC+pKbmEGh1a2bMuSr99eusz8rjaD5vAbuuJzg/VtmeSm+I+so02N6LbTXb4N1I+hRS841sAwY3EcEO3IECPrRXqlxIgdUN30KgFnIjMPnbp7MGOqUBaYzAGTvC2v5eFCAIqNLoaz8IS3KCK61b2uusbnJa2H5ltp2VPrO08t0jf69Hw2C1f34e/ywa5eEMQ9fTo34MMs5VODRErdqPBawtF9zaymGI4LlKab8cErB4NAUDIewfXsRyEtB5R3klRUsqivdIM+dinUc3HMx2XPf04jQF8z5b/iRo0CeWAXEWK2V1cxgqcJH7Itx2sm7KXkfH1u9J9fM87+EV'
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
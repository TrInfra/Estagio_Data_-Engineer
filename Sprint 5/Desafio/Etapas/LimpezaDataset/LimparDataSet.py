import pandas as pd

arquivo_entrada = r'C:\Users\raimu\OneDrive\Área de Trabalho\CompassUOL\Compass\Sprint 5\Desafio\Etapas\LimpezaDataset\V_OCORRENCIA_AMPLA.csv'

try:
    df = pd.read_csv(arquivo_entrada, delimiter=';', skiprows=1, encoding='utf-8')

    # Filtrar e limpar os dados
    
    # Remover linhas onde "Operador_Padronizado" é nulo
    df = df[df['Operador_Padronizado'].notna()]

    # Remover linhas onde "Numero_da_Ficha" tem caracteres especiais ou letras
    df = df[df['Numero_da_Ficha'].str.isdigit()]

    # Remover linhas onde "Hora_da_Ocorrencia" é nulo
    df = df[df['Hora_da_Ocorrencia'].notna()]
    
    #remover linhas que tenham numero de ocorrencia igual
    df = df.drop_duplicates(subset='Numero_da_Ocorrencia')
    
    # Substituir as aspas e as vírgulas por uma string vazia
    df['Historico'] = df['Historico'].str.replace('"', '')
    df['Historico'] = df['Historico'].str.replace(',', '')

    # Substituir quebras de linha por um espaço
    df['Historico'] = df['Historico'].str.replace('\n', ' ')

    
    # Caminho do arquivo de saída
    arquivo_saida = r'C:\Users\raimu\OneDrive\Área de Trabalho\CompassUOL\Compass\Sprint 5\Desafio\Etapas\LimpezaDataset\V_OCORRENCIA_AMPLA_Cleaned.csv'

    # Salvar o DataFrame limpo em um novo arquivo CSV com delimitador de vírgula
    df.to_csv(arquivo_saida, index=False, sep=',')

    print("Arquivo CSV limpo salvo com sucesso!")

except pd.errors.ParserError as e:
    print(f"Erro ao tentar ler o arquivo CSV: {e}")

    # Tentar ler o arquivo em blocos menores
    chunk_size = 100
    try:
        for chunk in pd.read_csv(arquivo_entrada, delimiter=';', skiprows=1, chunksize=chunk_size):
            print(chunk)
    except Exception as e:
        print(f"Erro: {e}")

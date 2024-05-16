import os

# Localização do arquivo
local_arquivo = os.path.dirname(os.path.abspath(__file__))


class AtorInfo:
    def __init__(self, nome, receita_total, num_filmes, media_por_filme, filme_principal, receita_filme_principal):
        self.nome = nome
        self.receita_total = receita_total
        self.num_filmes = num_filmes
        self.media_por_filme = media_por_filme
        self.filme_principal = filme_principal
        self.receita_filme_principal = receita_filme_principal

def limpar_dados(linha):
    campos = linha.strip().split(',')
    nome = ','.join(campo.replace('"', '') for campo in campos[:-5])
    receita_total = float(campos[-5].replace(',', ''))
    num_filmes = int(campos[-4])
    media_por_filme = float(campos[-3])
    filme_principal = campos[-2]
    receita_filme_principal = float(campos[-1].replace(',', ''))
    return AtorInfo(nome, receita_total, num_filmes, media_por_filme, filme_principal, receita_filme_principal)


def encontrar_ator_com_mais_filmes(dados_limpos):
    mais_filmes = 0
    ator_com_mais_filmes = ''
    for ator in dados_limpos:
        if ator.num_filmes > mais_filmes:
            mais_filmes = ator.num_filmes
            ator_com_mais_filmes = ator.nome

    return ator_com_mais_filmes, mais_filmes

def encontrar_ator_com_maior_media(dados_limpos):
    maior_media = 0
    ator_com_maior_media = ''
    for ator in dados_limpos:
        if ator.media_por_filme > maior_media:
            maior_media = ator.media_por_filme
            ator_com_maior_media = ator.nome
    return ator_com_maior_media, maior_media

def contar_aparicoes_filmes(dados_limpos):
    contagem_filmes = {}
    for ator in dados_limpos:
        if ator.filme_principal in contagem_filmes:
            contagem_filmes[ator.filme_principal] += 1
        else:
            contagem_filmes[ator.filme_principal] = 1

    filmes_ordenados = sorted(contagem_filmes.items(), key=lambda x: (-x[1], x[0]))

    return filmes_ordenados

def escrever_atores_por_receita_total(dados_limpos, arquivo_saida):
    atores_ordenados = sorted(dados_limpos, key=lambda x: x.receita_total, reverse=True)
    with open(arquivo_saida, 'w') as arquivo:
        for ator in atores_ordenados:
            arquivo.write(f'{ator.nome} - R$ {ator.receita_total:.2f}\n')

# Limpeza dos dados e leitura do arquivo CSV
dados_limpos = []
with open(os.path.join(local_arquivo, "actors.csv"), "r") as arquivoCSV:
    next(arquivoCSV)  # Ignorar a primeira linha (cabeçalho)
    for linha in arquivoCSV:
        linha = linha.strip()
        if linha:
            try:
                dados_limpos.append(limpar_dados(linha))
            except (ValueError, IndexError):
                print(ValueError)
                pass

# Etapa 1
ator_com_mais_filmes, num_filmes_max = encontrar_ator_com_mais_filmes(dados_limpos)
with open(os.path.join(local_arquivo, "Etapa-1.txt"), "w") as etapa_1_arquivo:
    etapa_1_arquivo.write(f'{ator_com_mais_filmes} - {num_filmes_max} filmes')

# Etapa 2
receita_total = sum(ator.receita_filme_principal for ator in dados_limpos)
num_atores = len(dados_limpos)
media_receita = receita_total / num_atores 
with open(os.path.join(local_arquivo, "Etapa-2.txt"), "w") as etapa_2_arquivo:
    etapa_2_arquivo.write(f"A média de receita de bilheteria bruta dos principais filmes, considerando todos os atores, é de R$ {media_receita:.2f} milhões.")

# Etapa 3
ator_com_maior_media, media_maxima = encontrar_ator_com_maior_media(dados_limpos)
with open(os.path.join(local_arquivo, "Etapa-3.txt"), "w") as etapa_3_arquivo:
    etapa_3_arquivo.write(f'{ator_com_maior_media} - R$ {media_maxima:.2f} de média por filme')

# Etapa 4
filmes_ordenados = contar_aparicoes_filmes(dados_limpos)
with open(os.path.join(local_arquivo, "Etapa-4.txt"), "w") as etapa_4_arquivo:
    for index, (filme, contagem) in enumerate(filmes_ordenados, start=1):
        etapa_4_arquivo.write(f'{index}. O filme {filme} aparece {contagem} vez(es) no dataset\n')

# Etapa 5
escrever_atores_por_receita_total(dados_limpos, os.path.join(local_arquivo, "Etapa-5.txt"))

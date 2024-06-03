import os

local_arquivo = os.path.dirname(os.path.abspath(__file__))

def processar_notas():
    estudantes = []

    with open(os.path.join(local_arquivo, "estudantes.csv"), "r") as csvfile:
        for row in csvfile:
           
            dados = row.strip().split(',')
            nome = dados[0]
            notas = list(map(int, dados[1:]))
            estudantes.append((nome, notas))

    relatorio = []

    for nome, notas in estudantes:
        
        tres_maiores_notas = sorted(notas, reverse=True)[:3]
        
        
        media = round(sum(tres_maiores_notas) / 3, 2)
        
        
        relatorio.append(f"Nome: {nome} Notas: {tres_maiores_notas} Média: {media}")

    
    relatorio.sort()

    
    for linha in relatorio:
        print(linha)

processar_notas()
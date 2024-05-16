'''
Exercícios Parte 2
Leia o arquivo person.json, faça o parsing e imprima seu conteúdo.

Dica: leia a documentação do pacote json
'''

import json
import os
local_arquivo= os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(local_arquivo, "person.json"), "r") as arquivo_json:
    dados_json = json.load(arquivo_json)
    
JsonFormatado = json.dumps(dados_json).replace('"', "'")
print(JsonFormatado)
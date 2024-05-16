'''
Exercícios Parte 2
Escreva um programa que lê o conteúdo 
do arquivo texto arquivo_texto.txt e 
imprime o seu conteúdo.
'''
import os
local_arquivo= os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(local_arquivo, "arquivo_texto.txt"), "r") as arquivo:
    conteudo = arquivo.read().rstrip("\n")

print(conteudo,end ="")
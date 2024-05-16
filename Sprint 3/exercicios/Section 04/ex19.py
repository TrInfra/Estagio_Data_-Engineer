'''
Exercícios Parte 2
Calcule o valor mínimo, valor máximo, valor médio e a mediana da lista gerada na célula abaixo:

Obs.: Lembrem-se, para calcular a mediana a lista deve estar ordenada!

import random 
# amostra aleatoriamente 50 números do intervalo 0...500
random_list = random.sample(range(500),50)

Use as variáveis abaixo para representar cada operação matemática:

mediana
media
valor_minimo 
valor_maximo 

Importante: Esperamos que você utilize as funções abaixo em seu código:

random
max
min
sum
'''

import random

random_list = sorted(random.sample(range(500), 50))

def Calcularmediana (mediana):
    tamanho = len(random_list)
    mediana = (random_list[tamanho // 2 - 1] + random_list[tamanho // 2]) / 2
    return mediana
    
    
mediana = Calcularmediana(random_list)
soma= sum(random_list)
media = soma/50
valor_minimo = min(random_list)
valor_maximo = max(random_list)

print(f"Media: {media}, Mediana: {mediana}, Mínimo: {valor_minimo}, Máximo: {valor_maximo}")
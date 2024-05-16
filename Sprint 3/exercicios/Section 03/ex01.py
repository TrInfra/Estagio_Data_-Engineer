'''

Exercícios Parte 1
Desenvolva um código em Python que crie variáveis para armazenar 
o nome e a idade de uma pessoa, juntamente com seus valores correspondentes.
Como saída, imprima o ano em que a pessoa completará 100 anos de idade.
'''
import datetime
nome = "Nycolas"
idade = 19

ano_atual = datetime.datetime.now().year
ano_100 = ano_atual + (100 - idade)

print(ano_100)
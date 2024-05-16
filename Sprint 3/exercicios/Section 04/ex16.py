'''
Exercícios Parte 2
Escreva uma função que recebe uma string de números separados por vírgula e retorne a soma de todos eles. Depois imprima a soma dos valores.

A string deve ter valor  "1,3,4,6,10,76"
'''

def somarNum(Num):
    numero = Num.split(",")
    soma = sum(map(int, numero))
    return soma    

Num = "1,3,4,6,10,76"
resultado = somarNum(Num)
print(resultado)
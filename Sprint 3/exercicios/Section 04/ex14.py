'''
Exercícios Parte 2
Escreva uma função que recebe um número variável de parâmetros não nomeados
e um número variado de parâmetros nomeados e imprime o valor de cada parâmetro
recebido.

Teste sua função com os seguintes parâmetros:

(1, 3, 4, 'hello', parametro_nomeado='alguma coisa', x=20)
'''

def imprimir_parametros(*args, **kwargs):
    # Imprimir os parâmetros não nomeados
    for arg in args:
        print( arg, end="\n")
    
    # Imprimir os parâmetros nomeados
    for valor in kwargs.values():
        print(valor, end="\n")

# Testar a função com os parâmetros fornecidos
imprimir_parametros(1, 3, 4, 'hello', parametro_nomeado='alguma coisa', x=20)
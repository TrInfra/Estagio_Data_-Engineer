'''
Exercícios Parte 2
Verifique se cada uma das palavras da lista ['maça', 'arara', 'audio', 'radio', 'radar', 'moto'] é ou não um palíndromo.

Obs: Palíndromo é uma palavra que permanece igual se lida de traz pra frente.



É necessário que você imprima no console exatamente assim:



A palavra: maça não é um palíndromo
 
A palavra: arara é um palíndromo
 
A palavra: audio não é um palíndromo
 
A palavra: radio não é um palíndromo
 
A palavra: radar é um palíndromo
 
A palavra: moto não é um palíndromo
'''

def palin(palavra):
    palavra = palavra.replace(" ", "").lower()
    return palavra == palavra[::-1]
    
a = ['maça', 'arara', 'audio', 'radio', 'radar', 'moto'] 

for p in a:
    if palin(p):
        print(f"A palavra: {p} é um palíndromo")
    else:
        print(f"A palavra: {p} não é um palíndromo")
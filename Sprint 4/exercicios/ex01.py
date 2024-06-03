import os 
local_arquivo = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(local_arquivo, "number.txt"), "r") as arquivo:
    numeros = list(map(int, arquivo.readlines()))
    
numeros_pares = list(filter(lambda x: x % 2 == 0, numeros))
numeros_pares_ordenados = sorted(numeros_pares, reverse=True)
cinco_maiores_pares = numeros_pares_ordenados[:5]
soma_cinco_maiores_pares = sum(cinco_maiores_pares)

print(cinco_maiores_pares)
print(soma_cinco_maiores_pares)
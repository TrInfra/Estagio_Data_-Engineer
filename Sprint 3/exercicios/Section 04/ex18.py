'''

Exercícios Parte 2
Dado o dicionário a seguir:

speed = {'jan':47, 'feb':52, 'march':47, 'April':44, 'May':52, 'June':53, 'july':54, 'Aug':44, 'Sept':54}

Crie uma lista com todos os valores (não as chaves!) e coloque numa lista de forma que não haja valores duplicados.
'''

speed = {'jan':47, 'feb':52, 'march':47, 'April':44, 'May':52, 'June':53, 'july':54, 'Aug':44, 'Sept':54}

Speed_set = set(speed.values())

def CriarList (speed):
    lista = []
    for i in Speed_set:
        lista.append(i)
    return lista
    
print(CriarList(Speed_set))
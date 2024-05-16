'''
Exercícios Parte 2
Escreva uma função que recebe como parâmetro uma 
lista e retorna 3 listas: a lista recebida dividida em 3 partes iguais. 
Teste sua implementação com a lista abaixo

lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
'''

def CriarList (lista):
    tamanhoLista = len(lista)
    dividirL = tamanhoLista//3
    lista01 = lista[:dividirL]
    lista02 = lista[dividirL:dividirL*2]
    lista03 = lista[dividirL*2:]
    return lista01, lista02 ,lista03

lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
lista01, lista02 ,lista03 = CriarList(lista)

saida01 = str(lista01).strip(',')
saida02 = str(lista02).strip(',')
saida03 = str(lista03).strip(',')
saidaF = saida01+ " " + saida02 + " " + saida03


print(saidaF)
'''
Exercícios Parte 2
Escreva uma função que recebe uma lista e retorna uma nova lista sem elementos duplicados. Utilize a lista a seguir para testar sua função.



['abc', 'abc', 'abc', '123', 'abc', '123', '123']
'''

a = ['abc', 'abc', 'abc', '123', 'abc', '123', '123']

set_a = set(a)
b = []
for i in set_a:
    b.append(i)
    
print(b)
'''
Exercícios Parte 1
Crie uma classe  Calculo  que contenha um método que aceita dois parâmetros, X e Y, e retorne a soma dos dois. Nessa mesma classe, implemente um método de subtração, que aceita dois parâmetros, X e Y, e retorne a subtração dos dois (resultados negativos são permitidos).

Utilize os valores abaixo para testar seu exercício:
x = 4 
y = 5
imprima:
Somando: 4+5 = 9
Subtraindo: 4-5 = -1
'''

class Calculo:
    def soma (self, x, y):
        self.x = x
        self.y = y
        resultado = x + y
        return resultado
    
    def subtracao(self, x, y):
        self.x = x
        self.y = y
        resultado = x - y
        return resultado
calculo = Calculo()        
print("Somando: 4+5 = ",calculo.soma(4,5))
print("Somando: 4-5 = ",calculo.subtracao(4,5))
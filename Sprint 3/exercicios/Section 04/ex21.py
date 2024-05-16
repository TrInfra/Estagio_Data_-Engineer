'''
Exercícios Parte 1
Implemente duas classes, Pato e Pardal , que herdam de uma superclasse chamada
Passaro as habilidades de voar e emitir som.

Contudo, tanto Pato quanto Pardal devem emitir sons diferentes (de maneira escrita) no console, conforme o modelo a seguir.
'''

class Passaro:
    def Voar(self):
        print("Voando...")
    
    def emitirSom(self):
        print("emitindo som")
    
class Pato(Passaro):
    def emitirSom(self):
        print("Pato emitindo som...")
        print("Quack Quack")
class Pardal(Passaro):
    def emitirSom(self):
        print("Pardal emitindo som...")
        print("Piu Piu")
    
pato = Pato()
print("Pato")
pato.Voar()
pato.emitirSom()
print("Pardal")
pardal = Pardal()
pardal.Voar()
pardal.emitirSom()
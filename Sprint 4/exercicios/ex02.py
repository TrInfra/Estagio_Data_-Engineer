def conta_vogais(texto: str) -> int:
    vogais = 'aeiouAEIOU'
    
    apenas_vogais = filter(lambda x: x in vogais, texto)
    
    return len(list(apenas_vogais))

print(conta_vogais("Ola mundo"))  
print(conta_vogais("Python"))       
print(conta_vogais("AEIOUaeiou"))  
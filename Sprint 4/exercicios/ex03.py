from functools import reduce

def calcula_saldo(lancamentos) -> float:
    valores = map(lambda x: -x[0] if x[1] == 'D' else x[0], lancamentos)
    
    saldo_final = reduce(lambda acc, x: acc + x, valores, 0)
    
    return saldo_final

lancamentos = [
    (200, 'D'),
    (300, 'C'),
    (100, 'C')
]
print(calcula_saldo(lancamentos)) 
def calcular_valor_maximo(operadores, operandos) -> float:
    operacoes = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b,
        '%': lambda a, b: a % b
    }

    resultados = map(lambda op_pair: operacoes[op_pair[0]](op_pair[1][0], op_pair[1][1]), zip(operadores, operandos))
    return max(resultados)

operadores = ['+','-','*','/','+']
operandos  = [(3, 6), (-7, 4.9), (8, -8), (10, 2), (8, 4)]
print(calcular_valor_maximo(operadores, operandos)) 
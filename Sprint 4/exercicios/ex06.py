def maiores_que_media(conteudo: dict) -> list:
    
    if not conteudo:  # Verifica se o dicionário está vazio
        return []
    
    soma_precos = sum(conteudo.values())
    quantidade_produtos = len(conteudo)
    media_precos = soma_precos / quantidade_produtos

    
    produtos_acima_da_media = [(nome, preco) for nome, preco in conteudo.items() if preco > media_precos]

    
    produtos_acima_da_media.sort(key=lambda item: item[1])

    
    return produtos_acima_da_media
    
conteudo = {
    "arroz": 4.99,
    "feijão": 3.49,
    "macarrão": 2.99,
    "leite": 3.29,
    "pão": 1.99
}

resultado = maiores_que_media(conteudo)
print(resultado)

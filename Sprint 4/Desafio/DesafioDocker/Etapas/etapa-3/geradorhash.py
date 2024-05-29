import hashlib

while True:
    message = (input("Digite uma mensagem ou 'exit' para sair:  "))

    if message.lower() == 'exit':
        print("Saindo...")
        break
    result = hashlib.sha1(message.encode('utf-8'))

    print("HASH: ",result.hexdigest())



## Programação Funcional

### Composição de função
Composição de funções é criar uma nova função através da composição de outras. Por exemplo, vamos criar uma função que vai filtrar um array, filtrando somente os números pares e multiplicando por dois:

```python
numeros = [2, 3, 4, 5, 6, 7, 8, 9, 10]
resultado = list(map(lambda numero: numero * 2, filter(lambda numero: numero % 2 == 0, numeros)))

print(resultado)
# [ 4, 8, 12, 16, 20 ]
```

### Funções Puras

Uma função é chamada pura quando invocada mais de uma vez produz exatamente o mesmo resultado. Isto é, o retorno da função é sempre o mesmo se você passar os mesmos parâmetros, então ela não pode depender de valores mutáveis. Por outro lado, ela não pode causa efeitos colaterais externos, pois se ela imprime uma linha de saída, altera algo no banco, lança um foguete para o espaço, ao invocá-la a segunda vez ela vai causar um novo efeito.

```python
def verfica_se_e_maior_que(entrada1, entrada2):
    return entreda1 >= entrada2

print(verifica_se_e_maior_que(13, 13))  # True

```

### Características da função pura em Python:
Determinística: A função verifica_se_e_maior_que sempre retornará o mesmo resultado se receber os mesmos argumentos. Neste caso, a função retornará True ou False dependendo se entrada1 é maior ou igual a entrada2.

Sem efeitos colaterais: A função não modifica nenhuma variável ou estado externo. Não faz impressões, não altera bases de dados, não lança foguetes etc.

Sem dependências de estado externo: A função não depende de variáveis fora do seu escopo, apenas dos parâmetros que recebe.


### Imutabilidade

Imutabilidade significa que uma vez que uma variável que recebeu um valor, vai possuir esse valor para sempre, ou quando criamos um objeto ele não pode ser modificado.

```python
sobre_nome = "Silveira"

# Realiza a substituição e retorna uma nova string
novo_sobre_nome = sobre_nome.replace("Silveira", "Souza")

# Imprime as strings para mostrar a imutabilidade
print(novo_sobre_nome)  # Saída: 'Souza'
print(sobre_nome)       # Saída: 'Silveira'

```

### Explicação:
Imutabilidade de strings em Python:

Quando você cria uma string, ela não pode ser modificada. Qualquer método que parece modificar a string (como replace) na verdade retorna uma nova string.
Exemplo explicado:

sobre_nome é uma string inicializada com o valor "Silveira".
Quando chamamos sobre_nome.replace("Silveira", "Souza"), uma nova string "Souza" é criada e atribuída à variável novo_sobre_nome.
A string original sobre_nome permanece inalterada, mantendo o valor "Silveira".


### Imperativo x Declarativo
É muito comum aprender a programar de forma imperativa, onde mandamos alguém fazer algo. Busque o usuário 15 no banco de dados. Valide essas informações do usuário.

Na programação funcional tentamos programar de forma declarativa, onde declaramos o que desejamos, sem explicitar como será feito. Qual o usuário 15? Quais os erros dessas informações?

### Estado compartilhado

Estado compartilhado é qualquer valor que está acessível por mais de um ponto de uma aplicação. Por exemplo:

```python
# Variável global representando o estado compartilhado
idade = 31

# Função que utiliza a variável global
def calcula_idade_dos_irmaos(idade_irmao):
    return idade + idade_irmao

# Exemplos de uso
print(calcula_idade_dos_irmaos(10))  # Saída: 41
print(calcula_idade_dos_irmaos(15))  # Saída: 46

```
### Explicação:
Variável Global:

idade é uma variável global que representa o estado compartilhado.
Função Dependente do Estado Compartilhado:

A função calcula_idade_dos_irmaos usa a variável global idade para calcular a idade dos irmãos.
Isso significa que o resultado da função depende não apenas do argumento idade_irmao, mas também do estado da variável idade.
Impressão dos Resultados:

Ao chamar calcula_idade_dos_irmaos com diferentes valores de idade_irmao, a função soma esses valores ao estado compartilhado idade e retorna o resultado.


### Comando Para Criar uma imagem no docker
    docker build -t meu-projeto .
### Comando Para executar um container a partir da imagem criada.
    docker run meu-projeto

## 1. Usar o Modo Interativo do Docker
Você pode iniciar um contêiner em modo interativo com um shell, permitindo que você execute comandos dentro do contêiner sem precisar criar um novo toda vez.
    
    docker exec -it <id> bash -> caso já exista
    docker run -it --name meu-projeto-container meu-projeto bash
Depois de entrar no contêiner, você pode executar o script carguru.py quantas vezes quiser:

    python carguru.py
Quando quiser sair do contêiner, você pode digitar exit, e o contêiner será parado, mas ainda estará disponível para ser reiniciado.

## 2. Reiniciar um Contêiner Parado
Se você já criou um contêiner e parou ele, pode reiniciá-lo e executá-lo novamente. Primeiro, você deve iniciar o contêiner, depois pode executar o script dentro dele.

Primeiro, crie e inicie o contêiner nomeando-o para reutilização:

    docker run -d --name meu-projeto-container meu-projeto
Para executar o script, você pode usar o comando docker exec:
    
    docker exec meu-projeto-container python carguru.py

## Comandos

Você pode obter arquivos da internet por meio do comando wget em seu container.
```
os.system("wget --header='Authorization: token <Seu Token>' <Seu URL do README.md>")
``` 

Usando o Spark Shell, apresente a sequência de comandos Spark necessários para contar a quantidade de ocorrências de cada palavra contida no arquivo README.md de seu repositório git.

iniciar o Pyspark
```shell
pyspark
```
Carregar o arquivo `README.md` no RDD ``(Resilient Distributed Dataset)`` usando o contexto Spark (sc). O arquivo é lido linha por linha.
```python
readme_rdd = sc.textFile("<caminho até seu arquivo aqui>")
```
Contar as palavras:
```python
contagem_de_palavras = readme_rdd \
.flatMap(lambda linha: linha.split()) \ # Divide cada linha do arquivo em palavras.
.map(lambda palavra: palavra.lower()) \ # Converte todas as palavras para minúsculas para garantir que a contagem não seja sensível a maiúsculas/minúsculas
.filter(lambda palavra: palavra) \ # Remove quaisquer palavras vazias resultantes de quebras de linha ou espaços em branco.
.map(lambda palavra: (palavra, 1)) \ # Isso prepara as palavras para a contagem, onde cada palavra é uma chave e 1 é o valor inicial.
.reduceByKey(lambda a, b: a + b) # Conta o número de ocorrências de cada palavra.
```

Vizualizar o resultado:

```python
for palavra, count in contagem_de_palavras.collect():
    print(f"{palavra}: {count}")
```
-- Criando a tabela e as colunas
CREATE EXTERNAL TABLE IF NOT EXISTS meubanco.person (
  nome varchar(180),
  sexo char(1),
  total integer,
  ano integer
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
 'serialization.format' = ',',
 'field.delim' = ','
)
LOCATION 's3://exercicio01sprint6.com/dados/';



-- Tarefa: Crie uma consulta que lista os 3 nomes mais usados em cada década desde 1950 até hoje.

SELECT 
    sub.decada,
    sub.nome,
    sub.total_decada
FROM (
    SELECT 
        nome,
        (ano / 10) * 10 AS decada,
        SUM(total) AS total_decada,
        ROW_NUMBER() OVER (PARTITION BY (ano / 10) * 10 ORDER BY SUM(total) DESC) AS posicao
    FROM 
        person
    WHERE 
        ano >= 1950
    GROUP BY 
        nome, (ano / 10) * 10
) AS sub
WHERE 
    sub.posicao <= 3
ORDER BY 
    sub.decada, sub.posicao;
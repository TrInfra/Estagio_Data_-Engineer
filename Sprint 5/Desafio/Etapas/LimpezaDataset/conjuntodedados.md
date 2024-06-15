## Sobre o dataset:
O dataset escohido foi o da Agência Nacional de Aviação Civil ```(ANAC)``` que trata de acidentes com aeronaves, nele contém no total 45 colunas, foram utilizadas apenas as colunas:    
``` Ilesos_Tripulantes, Data_da_Ocorrencia, Classificacao_da_Ocorrencia, UF, Regiao ```

## Sobre a consulta ``` (QUERY) ```
Foi pedido que apresentássemos as seguintes funções dentro da nossa query:

- ``2`` Funções de Agregação
- ``1`` Função Condicional
- ``1`` Função de Conversão
- ``1`` Função de Data
- ``1`` Função de String

```SQL
SELECT 
    MAX(CAST(NULLIF(s."Ilesos_Tripulantes", '') AS FLOAT)) AS Maior_valor_IlesosTripulantes,
    AVG(CAST(NULLIF(s."Ilesos_Tripulantes", '') AS FLOAT)) AS Media_IlesosTripulantes 
FROM s3object s
WHERE
    EXTRACT(
        MONTH
        FROM
        UTCNOW()
        ) = CAST(SUBSTRING(s."Data_da_Ocorrencia", 6, 2) AS INTEGER)
AND (
    CASE
    WHEN s."Classificacao_da_Ocorrencia" = 'Incidente Grave' THEN 'Muito Grave' 
    WHEN s."Classificacao_da_Ocorrencia" = 'Acidente' THEN 'Pouco Grave' 
    ELSE s."Classificacao_da_Ocorrencia" 
    END) = 'Muito Grave'
AND s."UF" = 'PR' OR s."Regiao" = 'Sudeste'
```

A consulta acima tem como objetivo calcular o valor máximo e a média do número de tripulantes ilesos em ocorrências classificadas como "Muito Grave" que ocorreram no estado do Paraná (PR) ou na região Sudeste. A consulta é filtrada para incluir apenas ocorrências do mês atual.

## Resultado da consulta

| Maior_valor_IlesosTripulantes |Media_IlesosTripulantes  |
|----------|----------|
| 6.0  | 1.3  |



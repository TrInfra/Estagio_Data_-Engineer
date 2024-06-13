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


/* 
Query em uma só linha, para testar no S3 SELECT

SELECT MAX(CAST(NULLIF(s."Ilesos_Tripulantes", '') AS FLOAT)) AS Maior_valor_IlesosTripulantes, AVG(CAST(NULLIF(s."Ilesos_Tripulantes", '') AS FLOAT)) AS Media_IlesosTripulantes FROM s3object s WHERE EXTRACT( MONTH FROM UTCNOW() ) = CAST(SUBSTRING(s."Data_da_Ocorrencia", 6, 2) AS INTEGER) AND ( CASE WHEN s."Classificacao_da_Ocorrencia" = 'Incidente Grave' THEN 'Muito Grave' WHEN s."Classificacao_da_Ocorrencia" = 'Acidente' THEN 'Pouco Grave' ELSE s."Classificacao_da_Ocorrencia" END) = 'Pouco Grave' AND s."UF" = 'PR' OR s."Regiao" = 'Sudeste'
*/


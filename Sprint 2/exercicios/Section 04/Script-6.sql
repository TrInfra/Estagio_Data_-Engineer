--E08
--Apresente a query para listar o código e o nome do vendedor com maior número de vendas (contagem), e que estas vendas estejam com o status concluída. 
--As colunas presentes no resultado devem ser, portanto, cdvdd e nmvdd.

SELECT
    vendedor.cdvdd,
    vendedor.nmvdd
FROM
    tbvendedor AS vendedor
JOIN
    tbvendas AS venda ON vendedor.cdvdd = venda.cdvdd
WHERE
    venda.status = 'Concluído'
GROUP BY
    vendedor.cdvdd, vendedor.nmvdd
ORDER BY
    COUNT(venda.cdven) DESC
LIMIT 1;

--E09
--Apresente a query para listar o código e nome do produto mais vendido entre as datas de 2014-02-03 até 2018-02-02, e que estas vendas estejam com o status concluída.
--As colunas presentes no resultado devem ser cdpro e nmpro. */

SELECT
    venda.cdpro,
    venda.nmpro
FROM
    tbvendas AS venda
WHERE
    venda.status = 'Concluído'
    AND venda.dtven BETWEEN '2014-02-03' AND '2018-02-02'
GROUP BY
    venda.cdpro, venda.nmpro
ORDER BY
    COUNT(venda.cdven) DESC
LIMIT 1;

-- E10
--A comissão de um vendedor é definida a partir de um percentual sobre o total de vendas (quantidade * valor unitário) por ele realizado.
--O percentual de comissão de cada vendedor está armazenado na coluna perccomissao, tabela tbvendedor. 
--Com base em tais informações, calcule a comissão de todos os vendedores, considerando todas as vendas armazenadas na base de dados com status concluído.
--As colunas presentes no resultado devem ser vendedor, valor_total_vendas e comissao. O valor de comissão deve ser apresentado em ordem decrescente arredondado na segunda casa decimal.*/

SELECT
    vendedor.nmvdd AS vendedor,
    ROUND(SUM(venda.qtd * venda.vrunt), 2) AS valor_total_vendas,
    ROUND(SUM(venda.qtd * venda.vrunt) * (vendedor.perccomissao / 100.00), 2) AS comissao
FROM
    tbvendedor AS vendedor
JOIN
    tbvendas AS venda ON vendedor.cdvdd = venda.cdvdd
WHERE
    venda.status = 'Concluído'
GROUP BY
    vendedor.nmvdd
ORDER BY
    comissao DESC;
   
-- E11
--Apresente a query para listar o código e nome cliente com maior gasto na loja.
--As colunas presentes no resultado devem ser cdcli, nmcli e gasto, esta última representando o somatório das vendas (concluídas) atribuídas ao cliente. */ 

SELECT
    venda.cdcli,
    venda.nmcli,
    SUM(venda.qtd * venda.vrunt) AS gasto
FROM
    tbvendas AS venda
WHERE
    venda.status = 'Concluído'
GROUP BY
    venda.cdcli, venda.nmcli
ORDER BY
    gasto DESC
LIMIT 1;

-- E12
--Apresente a query para listar código, nome e data de nascimento dos dependentes do vendedor com menor valor total bruto em vendas (não sendo zero). 
--As colunas presentes no resultado devem ser cddep, nmdep, dtnasc e valor_total_vendas.
--Observação: Apenas vendas com status concluído.

SELECT
    dependente.cddep,
    dependente.nmdep,
    dependente.dtnasc,
    vendedor.valor_total_vendas
FROM
    tbdependente AS dependente
JOIN
    (
        SELECT
            vendedor.cdvdd,
            vendedor.nmvdd,
            COALESCE(SUM(venda.qtd * venda.vrunt), 0) AS valor_total_vendas
        FROM
            tbvendedor AS vendedor
        LEFT JOIN
            tbvendas AS venda ON vendedor.cdvdd = venda.cdvdd
        WHERE
            venda.status = 'Concluído'
        GROUP BY
            vendedor.cdvdd, vendedor.nmvdd
        HAVING
            valor_total_vendas > 0
        ORDER BY
            valor_total_vendas ASC
        LIMIT 1
    ) AS vendedor ON dependente.cdvdd = vendedor.cdvdd;


-- E13
--Apresente a query para listar os 10 produtos menos vendidos pelos canais de E-Commerce ou Matriz (Considerar apenas vendas concluídas).  
--As colunas presentes no resultado devem ser cdpro, nmcanalvendas, nmpro e quantidade_vendas. */ 

SELECT
    venda.cdpro,
    venda.nmcanalvendas,
    venda.nmpro,
    SUM(venda.qtd) AS quantidade_vendas
FROM
    tbvendas AS venda
WHERE
    venda.status = 'Concluído'
    AND venda.deletado = 0
    --AND venda.cdcanalvendas IN ('Ecommerce','Matriz')
GROUP BY
    venda.cdpro, venda.nmcanalvendas, venda.nmpro
ORDER BY
    quantidade_vendas ASC
LIMIT 10; 

--E14
--Apresente a query para listar o gasto médio por estado da federação. 
--As colunas presentes no resultado devem ser estado e gastomedio. 
--Considere apresentar a coluna gastomedio arredondada na segunda casa decimal e ordenado de forma decrescente.
--Observação: Apenas vendas com status concluído.

SELECT
    estado,
    ROUND(AVG(qtd * vrunt), 2) AS gastomedio
FROM
    tbvendas
WHERE
    status = 'Concluído'
GROUP BY
    estado
ORDER BY
    gastomedio DESC;


--E15
--Apresente a query para listar os códigos das vendas identificadas como deletadas. 
--Apresente o resultado em ordem crescente.


SELECT
    cdven
FROM
    tbvendas
WHERE
    deletado = 1
ORDER BY
    cdven ASC;


--E16
--Apresente a query para listar a quantidade média vendida de cada produto agrupado por estado da federação.
--As colunas presentes no resultado devem ser estado e nmprod e quantidade_media. Considere arredondar o valor da coluna quantidade_media na quarta casa decimal.
--Ordene os resultados pelo estado (1º) e nome do produto (2º).
--Obs: Somente vendas concluídas.


SELECT
    estado,
    nmpro,
    ROUND(AVG(qtd), 4.00) AS quantidade_media
FROM
    tbvendas
WHERE
    status = 'Concluído'
GROUP BY
    estado, nmpro
ORDER BY
    estado ASC, nmpro ASC;







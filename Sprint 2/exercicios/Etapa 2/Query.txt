SELECT 
	editora.codeditora,
    	editora.nome,
	COUNT(livro.cod) AS QuantidadeLivros
FROM 
    livro
JOIN 
    editora ON livro.editora = editora.codeditora
JOIN 
    endereco ON editora.endereco = endereco.codendereco
GROUP BY 
    editora.codeditora
ORDER BY 
    QuantidadeLivros DESC
LIMIT 5;
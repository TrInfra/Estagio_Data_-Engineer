SELECT
    livro.cod,
    livro.titulo,
    livro.autor,
    autor.nome,
    livro.Valor,
    livro.editora,
    editora.nome
FROM
    livro
JOIN
    autor ON livro.autor = autor.codautor
JOIN
    editora ON livro.editora = editora.codeditora
ORDER BY
    livro.Valor DESC
LIMIT 10;
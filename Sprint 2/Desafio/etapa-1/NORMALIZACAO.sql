-- normalizando a base de dados...

create table Cliente(
	idCliente INT PRIMARY KEY,
	nomeCliente VARCHAR(100),
	cidadeCliente VARCHAR(100),
	estadoCliente VARCHAR(100),
	paisCliente VARCHAR(100)
);

create table Carro (
	idCarro INT PRIMARY KEY,
	kmCarro INT,
	classiCarro VARCHAR(100),
	marcaCarro VARCHAR(100),
	modeloCarro VARCHAR(100),
	anoCarro INT,
	idCombustivel int,
	FOREIGN KEY (idCombustivel) REFERENCES Combustivel(idCombustivel)
);


CREATE TABLE Combustivel (
    idCombustivel int PRIMARY KEY,
    tipoCombustivel varchar(100)
);

CREATE TABLE Vendedor (
    idVendedor int,
    nomeVendedor varchar(100),
    sexoVendedor varchar(100),
    estadoVendedor varchar(100)
);

CREATE TABLE Locacao_info (
    idLocacao int,
    dataLocacao date,
    horaLocacao time,
    qtdDiaria int,
    vlrDiaria decimal,
    dataEntrega date,
   	horaEntrega time,
   	kmCarro INT,
   	FOREIGN KEY (idlocacao) REFERENCES Locacao(idlocacao)
);

Create table locacao(
	idlocacao int,
	idCliente int,
	idCarro int,
	idVendedor int,
	FOREIGN KEY (idlocacao) REFERENCES Locacao_info(idCliente),
   	FOREIGN KEY (idCliente) REFERENCES Cliente(idCliente),
   	FOREIGN KEY (idCarro) REFERENCES Carro(idCarro),
   	FOREIGN KEY (idVendedor) REFERENCES Vendedor(idVendedor)
);

-- Depois de normalizar agora só falta enviar os dados para dentro da nova
-- base de dados normalizada

INSERT INTO Cliente(idCliente,nomeCliente,cidadeCliente,estadoCliente,paisCliente)
SELECT DISTINCT idCliente, nomeCliente ,cidadeCliente ,estadoCliente ,paisCliente 
FROM tb_locacao ;

INSERT INTO Carro (idCarro,kmCarro, classiCarro, marcaCarro,modeloCarro , anoCarro, idCombustivel)
SELECT DISTINCT idCarro,kmCarro, classiCarro, marcaCarro, modeloCarro, anoCarro, idCombustivel
FROM (
	SELECT idCarro, kmCarro, classiCarro, marcaCarro, modeloCarro, anoCarro, idCombustivel,
	ROW_NUMBER () OVER (PARTITION BY idCarro ORDER BY kmCarro DESC) AS row_num
	FROM tb_locacao
) AS subquery
WHERE row_num = 1; 

INSERT INTO Combustivel(idCombustivel, tipoCombustivel)
SELECT DISTINCT idCombustivel, tipoCombustivel
FROM tb_locacao;


INSERT INTO Vendedor ( idVendedor, nomeVendedor, sexoVendedor, estadoVendedor)
SELECT DISTINCT  idVendedor, nomeVendedor, sexoVendedor, estadoVendedor
FROM tb_locacao;

INSERT INTO Locacao_info  ( idLocacao , dataLocacao , horaLocacao , qtdDiaria, vlrDiaria,dataEntrega,horaEntrega, kmCarro)
SELECT DISTINCT  idLocacao , dataLocacao , horaLocacao , qtdDiaria, vlrDiaria,dataEntrega,horaEntrega, kmCarro 
FROM tb_locacao;

INSERT INTO locacao (idLocacao,idCliente,idCarro,idVendedor)
SELECT DISTINCT idLocacao,idCliente,idCarro,idVendedor
FROM tb_locacao;
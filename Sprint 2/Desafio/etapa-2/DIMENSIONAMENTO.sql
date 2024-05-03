--Criando as views para poder gerar o diagrama dimensional

CREATE VIEW Fato_Locacao AS
SELECT 
	LI.idLocacao ,
	LI.dataLocacao,
	LI.horaLocacao, 
	LI.qtdDiaria, 
	LI.vlrDiaria, 
	LI.dataEntrega, 
	LI.horaEntrega, 
	LI.kmCarro,
	C.idCliente,
	Ca.idCarro,
   	V.idVendedor
FROM Locacao L
JOIN Locacao_info LI 
JOIN Cliente C ON L.idCliente = C.idCliente
JOIN Carro Ca ON L.idCarro = Ca.idCarro
JOIN Vendedor V ON L.idVendedor = V.idVendedor;

CREATE VIEW Dim_Cliente AS
SELECT 
    idCliente,
    nomeCliente,
    cidadeCliente,
    estadoCliente,
    paisCliente
FROM Cliente;

CREATE VIEW Dim_Carro AS
SELECT 
    car.idCarro,
    car.kmCarro,
    car.classiCarro,
    car.marcaCarro,
    car.modeloCarro,
    car.anoCarro,
    Com.tipoCombustivel
FROM Carro AS car
LEFT JOIN combustivel AS com ON com.idcombustivel = car.idcombustivel;

CREATE VIEW Dim_Vendedor AS
SELECT 
    idVendedor,
    nomeVendedor,
    sexoVendedor,
    estadoVendedor
FROM Vendedor;

CREATE VIEW Dim_tempo AS
SELECT 
	li.dataLocacao,
    li.horaLocacao,
    li.dataEntrega,
   	li.horaEntrega 
FROM Locacao_info AS li;
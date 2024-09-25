CREATE DATABASE stocksync;

USE stocksync;

CREATE TABLE produtos (
    id_produto INT AUTO_INCREMENT PRIMARY KEY,
    nome_produto VARCHAR(255),
    preco DECIMAL(10, 2),
    quantidade INT,
    status CHAR(1)
);

CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nome_cliente VARCHAR(255),
    cpf CHAR(14),
    telefone VARCHAR(15), 
    email VARCHAR(255), 
    status CHAR(1)
);

CREATE TABLE pagamento (
    cod_pag INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(255)
);

CREATE TABLE vendas (
    id_venda INT AUTO_INCREMENT PRIMARY KEY,
    id_produto INT, -- FK referenciando produtos
    id_cliente INT, -- FK referenciando clientes
    cod_pag INT, -- FK referenciando pagamento
    quantidade INT,
    data DATE,
    status CHAR(1),
    FOREIGN KEY (id_produto) REFERENCES produtos(id_produto),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (cod_pag) REFERENCES pagamento(cod_pag)
);

import sqlite3;

conexao = sqlite3.connect('stocksync.db');
cursor = conexao.cursor();

cursor.execute('''CREATE TABLE IF NOT EXISTS  usuarios (
                  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                  nome TEXT NOT NULL,
                  senha TEXT NOT NULL);''');

cursor.execute(''' CREATE TABLE IF NOT EXISTS produtos (
                    id_produto INTEGER PRIMARY KEY AUTOINCREMENT, 
                    nome TEXT,
                    descricao TEXT,
                    quantidade INTEGER,
                    preco NUMERIC(5,2),
                    situacao INTEGER
               );''') 

cursor.execute('''INSERT INTO usuarios(nome,senha) values('admin','admin123');''')

conexao.commit();
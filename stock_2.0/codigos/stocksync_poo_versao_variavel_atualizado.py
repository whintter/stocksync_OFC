import sqlite3
import datetime
import openpyxl
import tkinter as tk
from tkinter import messagebox

# Conexão com banco de dados
class ConexaoBanco:
    def __init__(self, nome_banco: str = 'stocksync.db'):
        self.conexao = sqlite3.connect(nome_banco)
        self.cursor = self.conexao.cursor()

    def executar_comando(self, comando: str, parametros: tuple = None) -> None:
        if parametros:
            self.cursor.execute(comando, parametros)
        else:
            self.cursor.execute(comando)
        self.conexao.commit()

    def consultar_dados(self, comando: str, parametros: tuple = None) -> list:
        if parametros:
            self.cursor.execute(comando, parametros)
        else:
            self.cursor.execute(comando)
        return self.cursor.fetchall()

    def fechar_conexao(self) -> None:
        self.conexao.close()

# Classe Produto
class Produto:
    def __init__(self, id_produto: int, nome: str, quantidade: int, preco: float, situacao: int = 1):
        self.id_produto = id_produto
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco
        self.situacao = situacao

    def atualizar_quantidade(self, nova_quantidade: int):
        self.quantidade = nova_quantidade

# Classe GerenciarProdutos
class GerenciarProdutos:
    def __init__(self, banco: ConexaoBanco):
        self.banco = banco

    def criar_tabela(self):
        comando = '''CREATE TABLE IF NOT EXISTS produtos (
                        id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT,
                        quantidade INTEGER,
                        preco NUMERIC(5,2),
                        situacao INTEGER
                     );'''
        self.banco.executar_comando(comando)

    def cadastrar_produto(self, produto: Produto):
        comando = '''INSERT INTO produtos (nome, preco, quantidade, situacao) VALUES (?, ?, ?, ?)'''
        self.banco.executar_comando(comando, (produto.nome, produto.preco, produto.quantidade, produto.situacao))

    def listar_produtos(self):
        comando = '''SELECT id_produto, nome, quantidade, preco FROM produtos'''
        lista_produtos = self.banco.consultar_dados(comando)
        return lista_produtos
    

    def atualizar_quantidade(self, id_produto: int, nova_quantidade: int):
        comando = '''UPDATE produtos SET quantidade = ? WHERE id_produto = ?'''
        self.banco.executar_comando(comando, (nova_quantidade, id_produto))

# Classe Venda
class Venda:
    def __init__(self, produto: Produto, quantidade: int):
        self.produto = produto
        self.quantidade = quantidade
        self.preco_total = produto.preco * quantidade

    def processar_venda(self):
        if self.quantidade <= self.produto.quantidade:
            self.produto.atualizar_quantidade(self.produto.quantidade - self.quantidade)
            return self.preco_total
        else:
            raise ValueError("Quantidade insuficiente em estoque.")

# Classe GerenciarVendas
class GerenciarVendas:
    def __init__(self, banco: ConexaoBanco, gerenciar_produtos: GerenciarProdutos):
        self.banco = banco
        self.gerenciar_produtos = gerenciar_produtos

    def criar_tabela(self):
        comando = '''CREATE TABLE IF NOT EXISTS vendas (
                        id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome_produto TEXT,
                        quantidade INTEGER,
                        preco_total NUMERIC(5,2),
                        data_venda TEXT
                     );'''
        self.banco.executar_comando(comando)

    def cadastrar_venda(self, nome_produto: str, quantidade: int):
        produto = next((p for p in self.gerenciar_produtos.listar_produtos() if p[1] == nome_produto), None)
        if produto:
            id_produto = produto[0]
            quantidade_disponivel = produto[2]
            preco = produto[3]
            if quantidade <= quantidade_disponivel:
                preco_total = quantidade * preco
                data_venda = datetime.datetime.now().strftime("%d/%m/%Y")
                comando = '''INSERT INTO vendas (nome_produto, quantidade, preco_total, data_venda) 
                             VALUES (?, ?, ?, ?)'''
                self.banco.executar_comando(comando, (nome_produto, quantidade, preco_total, data_venda))
                self.gerenciar_produtos.atualizar_quantidade(id_produto, quantidade_disponivel - quantidade)
            else:
                raise ValueError("Quantidade insuficiente em estoque.")
        else:
            raise ValueError("Produto não encontrado.")

    def listar_vendas(self):
        comando = '''SELECT nome_produto, quantidade, preco_total, data_venda FROM vendas'''
        lista_vendas = self.banco.consultar_dados(comando);
        return lista_vendas

# Relatório de vendas
class Relatorio:
    @staticmethod
    def gerar_relatorio_excel(vendas: list) -> None:
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = "Vendas"
        sheet.append(["Produto", "Quantidade", "Preço Total", "Data"])

        for venda in vendas:
            sheet.append(venda)

        wb.save("relatorio_vendas.xlsx")
        print("Relatório exportado com sucesso para 'relatorio_vendas.xlsx'!")

# Interface gráfica com Tkinter
class InterfaceEstoque:
    def __init__(self, master):
        self.master = master
        self.master.title("Gerenciador de Estoque")
        self.master.geometry("700x600")

        self.banco = ConexaoBanco()
        self.gerenciar_produtos = GerenciarProdutos(self.banco)
        self.gerenciar_vendas = GerenciarVendas(self.banco, self.gerenciar_produtos)

        # Criando widgets
        self.criar_widgets()

        # Criando as tabelas no banco
        self.gerenciar_produtos.criar_tabela()
        self.gerenciar_vendas.criar_tabela()

    def criar_widgets(self):
        # Frame para Cadastro de Produtos
        self.frame_produto = tk.LabelFrame(self.master, text="Cadastro de Produto", padx=10, pady=10)
        self.frame_produto.pack(padx=10, pady=10, fill="both", expand=True)

        tk.Label(self.frame_produto, text="Nome do Produto:").grid(row=0, column=0)
        self.entry_nome_produto = tk.Entry(self.frame_produto)
        self.entry_nome_produto.grid(row=0, column=1)

        tk.Label(self.frame_produto, text="Preço do Produto:").grid(row=1, column=0)
        self.entry_preco_produto = tk.Entry(self.frame_produto)
        self.entry_preco_produto.grid(row=1, column=1)

        tk.Label(self.frame_produto, text="Quantidade do Produto:").grid(row=2, column=0)
        self.entry_quantidade_produto = tk.Entry(self.frame_produto)
        self.entry_quantidade_produto.grid(row=2, column=1)

        self.button_cadastrar_produto = tk.Button(self.frame_produto, text="Cadastrar Produto", command=self.cadastrar_produto)
        self.button_cadastrar_produto.grid(row=3, columnspan=2)

        # Frame para Cadastro de Vendas
        self.frame_venda = tk.LabelFrame(self.master, text="Venda", padx=10, pady=10)
        self.frame_venda.pack(padx=10, pady=10, fill="both", expand=True)

        tk.Label(self.frame_venda, text="Nome do Produto:").grid(row=0, column=0)
        self.entry_nome_produto_venda = tk.Entry(self.frame_venda)
        self.entry_nome_produto_venda.grid(row=0, column=1)

        tk.Label(self.frame_venda, text="Quantidade Vendida:").grid(row=1, column=0)
        self.entry_quantidade_venda = tk.Entry(self.frame_venda)
        self.entry_quantidade_venda.grid(row=1, column=1)

        self.button_cadastrar_venda = tk.Button(self.frame_venda, text="Cadastrar Venda", command=self.cadastrar_venda)
        self.button_cadastrar_venda.grid(row=2, columnspan=2)

        # Frame para Produtos e Vendas
        self.frame_produtos_vendas = tk.LabelFrame(self.master, text="Produtos Cadastrados e Vendas Realizadas", padx=10, pady=10)
        self.frame_produtos_vendas.pack(padx=10, pady=10, fill="both", expand=True)

        # Botões para listar produtos e vendas
        self.button_listar_produtos = tk.Button(self.frame_produtos_vendas, text="Listar Produtos", command=self.listar_produtos)
        self.button_listar_produtos.grid(row=0, column=0, padx=5, pady=5)

        self.button_listar_vendas = tk.Button(self.frame_produtos_vendas, text="Listar Vendas", command=self.listar_vendas)
        self.button_listar_vendas.grid(row=0, column=1, padx=5, pady=5)

        # Botão para gerar relatório
        self.button_gerar_relatorio = tk.Button(self.frame_produtos_vendas, text="Gerar Relatório de Vendas", command=self.gerar_relatorio)
        self.button_gerar_relatorio.grid(row=1, columnspan=2, pady=10)

        # Texto para mostrar informações
        self.texto_info = tk.Text(self.frame_produtos_vendas, height=10, width=80)
        self.texto_info.grid(row=2, columnspan=2, padx=5, pady=5)

    def cadastrar_produto(self):
        nome = self.entry_nome_produto.get()
        preco = self.entry_preco_produto.get()
        quantidade = self.entry_quantidade_produto.get()

        if nome and preco and quantidade:
            try:
                preco = float(preco)
                quantidade = int(quantidade)
                produto = Produto(id_produto=0, nome=nome, preco=preco, quantidade=quantidade)
                self.gerenciar_produtos.cadastrar_produto(produto)
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso.")
                self.entry_nome_produto.delete(0, tk.END)
                self.entry_preco_produto.delete(0, tk.END)
                self.entry_quantidade_produto.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Erro", "Preço e Quantidade devem ser números válidos.")
        else:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")

    def cadastrar_venda(self):
        nome_produto = self.entry_nome_produto_venda.get()
        quantidade = self.entry_quantidade_venda.get()

        if nome_produto and quantidade:
            try:
                quantidade = int(quantidade)
                self.gerenciar_vendas.cadastrar_venda(nome_produto, quantidade)
                messagebox.showinfo("Sucesso", "Venda registrada com sucesso.")
                self.entry_nome_produto_venda.delete(0, tk.END)
                self.entry_quantidade_venda.delete(0, tk.END)
            except ValueError as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")

    def listar_produtos(self):
        produtos = self.gerenciar_produtos.listar_produtos()
        self.texto_info.delete(1.0, tk.END)
        for produto in produtos:
            self.texto_info.insert(tk.END, f"ID: {produto[0]} | Nome: {produto[1]} | Quantidade: {produto[2]} | Preço: {produto[3]}\n")

    def listar_vendas(self):
        vendas = self.gerenciar_vendas.listar_vendas()
        self.texto_info.delete(1.0, tk.END)
        for venda in vendas:
            self.texto_info.insert(tk.END, f"Produto: {venda[0]} | Quantidade: {venda[1]} | Preço Total: {venda[2]} | Data: {venda[3]}\n")

    def gerar_relatorio(self):
        vendas = self.gerenciar_vendas.listar_vendas()
        Relatorio.gerar_relatorio_excel(vendas)

# Executando a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceEstoque(root)
    root.mainloop()

import customtkinter;
import sqlite3;
import os;
import tkinter.font as tkFont
from tkinter import messagebox, Tk, Label;
from PIL import Image, ImageTk;

customtkinter.set_appearance_mode("dark");
customtkinter.set_default_color_theme('dark-blue');

conexao = sqlite3.connect('stocksync.db');
cursor = conexao.cursor();
conexao = sqlite3.connect('stocksync.db');
cursor = conexao.cursor();

cursor.execute('''CREATE TABLE IF NOT EXISTS  usuarios (
                  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                  nome TEXT NOT NULL,
                  senha TEXT NOT NULL);''');

cursor.execute(''' CREATE TABLE IF NOT EXISTS produtos (
                    id_produto INTEGER PRIMARY KEY AUTOINCREMENT, 
                    nome TEXT,
                    quantidade INTEGER,
                    preco NUMERIC(5,2),
                    situacao INTEGER
               );''') 

cursor.execute('''INSERT INTO usuarios(nome,senha) values('admin','admin123');''')

conexao.commit();

#funcao que executa o  login
def login():
    #pegando valor do campo de texto
    nome = entry_login_nome.get();
    senha = entry_login_senha.get();

    #consulta no banco 
    cursor.execute('''SELECT nome FROM usuarios WHERE nome = ? and senha=?''',(nome,senha));
    usuario_login = cursor.fetchone();

    if nome and senha:
        if usuario_login!=None:
            menu();
        elif usuario_login==None:
            login_error();
    else:
        messagebox.showwarning('Atenção','Digite algo nos campos de usuario e senha!');

#evita loop no texto de erro
def login_error():
    global fail_login;
    if fail_login != None:
        fail_login.destroy();
    fail_login = customtkinter.CTkLabel(janela, text='Login falhou, senha ou usuario esta incorreto');
    fail_login.pack(padx=10,pady=10);
    
#funcao que executa o menu:
def menu():
    #destruir janela anterior 
    messagebox.showinfo('Login','Login efetuado com sucesso!!');
    
    #nova janela de menu

    janela.destroy();
    menu= customtkinter.CTk();
    menu.geometry("850x550+400+200");
    
    #criacao tabs
    tabview = customtkinter.CTkTabview(menu, width=850, height=550);
    tabview.pack();
    home_tab = tabview.add("Home");
    produto_tab = tabview.add("Cadastrar Produtos");
    geren_tab = tabview.add("Gerenciamento");
    tabview.tab("Home").grid_columnconfigure(0,weight=1);
    tabview.tab("Cadastrar Produtos").grid_columnconfigure(0,weight=2);
    tabview.tab("Gerenciamento").grid_columnconfigure(0,weight=3);
    #funcoes para conteudo das tabs do menu 
    home(home_tab);
    gerenciamento(geren_tab);
    cad_produtos(produto_tab);
    
    menu.mainloop();

#tab home 
def home(tabh_func):
    
    #FONTES USADAS:
    fonte_titulo_stocksync = customtkinter.CTkFont(family="Arial", size=30, weight="bold")
    fonte_corpo_stocksync = customtkinter.CTkFont(family="Arial", size=17)
    fonte_subtitulo_stocksync = customtkinter.CTkFont(family="Algerian", size=13, weight="bold")

    # Label para os textos na Home
    #titulo
    lbl_titulo_stocksync = customtkinter.CTkLabel(tabh_func, text='STOCKSYNC: Quem Somos!', font=fonte_titulo_stocksync);
    lbl_titulo_stocksync.pack(padx=10,pady=10);
    
    #corpo
    # Frame para o corpo do texto
    corpo_frame = customtkinter.CTkFrame(tabh_func)
    corpo_frame.pack(padx=10, pady=10, fill="both", expand=True)

    # Corpo do texto
    # Corpo do texto
    lbl_corpo_stocksync1 = customtkinter.CTkTextbox(corpo_frame, wrap="word", font=fonte_corpo_stocksync)
    lbl_corpo_stocksync1.pack(padx=10, pady=10, fill="both", expand=True)
    lbl_corpo_stocksync1.insert("1.0", '   A StockSync é um projeto acadêmico da matéria de Programação do professor Murilo. Neste projeto, devêmos utilizar todas as ferramentas disponíveis que aprendermos, desenvolvendo algo que mostre nossa evolução durante a evolução da matéria.\n   A StockSync consiste num sistema de gerenciamento de estoque, tentando ao máximo evitar a ruptura de estoque e aumentar a eficiência das vendas de nossos clientes.\n\n   Confira nossos desenvolvedores!')
    lbl_corpo_stocksync1.configure(state="disabled")

    image_paths = [
        os.path.join(os.path.dirname(__file__), 'images/arthur_araujo.jpg'),
        os.path.join(os.path.dirname(__file__), 'images/igor_mazeti.jpg'),
        os.path.join(os.path.dirname(__file__), 'images/douglas_hiroiti.jpg'),
        os.path.join(os.path.dirname(__file__), 'images/hedes_murilo.jpg')
    ]

    # Lista para armazenar as imagens convertidas para Tkinter
    tk_images = []

    # Redimensionando e convertendo as imagens
    for path in image_paths:
        image = Image.open(path)
        image = image.resize((100, 100), Image.BILINEAR)
        tk_image = ImageTk.PhotoImage(image)
        tk_images.append(tk_image)

    # Criando labels para exibir as imagens
    for i, tk_image in enumerate(tk_images):
        frame = customtkinter.CTkFrame(tabh_func);
        frame.place(x=135 + i * 160, y=300);

        image_label = customtkinter.CTkLabel(frame, image=tk_image, text="");
        image_label.image = tk_image;
        image_label.pack();

        # Adicionar subtítulo
        subtitle = ['Arthur A.', 'Igor M.', 'Douglas H.', 'Hedes M.'][i];
        lbl_subtitulo_stocksync = customtkinter.CTkLabel(frame, text=subtitle, font=fonte_subtitulo_stocksync);
        lbl_subtitulo_stocksync.pack(pady=(0, 0));
#aba gerenciament0  
def gerenciamento(tabg_func):
    global avisos_frame
    
    # Título da aba de gerenciamento
    gerenciamento_titulo = customtkinter.CTkLabel(tabg_func, text="Gerenciamento de Produtos", font=("Arial", 16, "bold"))
    gerenciamento_titulo.pack(pady=10, anchor='center')

    # Frame para o botão e área de avisos
    top_frame = customtkinter.CTkFrame(tabg_func)
    top_frame.pack(padx=10, pady=10, fill="x")

    # Exibir os produtos cadastrados na tabela (botão)
    gerenciar_btn = customtkinter.CTkButton(top_frame, text="Mostrar Tabela", command=janela_de_gerenciamento)
    gerenciar_btn.pack(pady=10, padx=10, side="left")

    # Área de avisos
    avisos_frame = customtkinter.CTkFrame(top_frame, corner_radius=10, border_color="gray", border_width=2)
    avisos_frame.pack(pady=10, padx=10, fill="both", expand=True, side="right")

    # Atualizar avisos
    gerenciar_btn = customtkinter.CTkButton(top_frame, text="atualizar avisos", command=avisos)
    gerenciar_btn.pack(pady=20, padx=10, side="left")
    avisos()

    # Frame para a tabela de produtos
    tabela_frame = customtkinter.CTkFrame(tabg_func)
    tabela_frame.pack(padx=10, pady=10, fill="both", expand=True)


def mudar_quantidade():
    pass;

def exibir_tabela():
    # Limpar qualquer widget existente no frame
    for widget in frame_rolavel.winfo_children():
        widget.destroy();

    # Cabeçalhos da tabela
    colunas = ["Nome", "Quantidade", "Preço"]
    for i, coluna in enumerate(colunas):
        header = customtkinter.CTkLabel(frame_rolavel, text=coluna, font=("Arial", 12, "bold"))
        header.grid(row=0, column=i, padx=10, pady=5, sticky="ew")

    # Consulta ao banco de dados
    cursor.execute('''SELECT nome, quantidade, preco FROM produtos''')
    produtos = cursor.fetchall()
    

    # Adicionar dados dos produtos à tabela
    for i, produto in enumerate(produtos):
        quantidade_atualizar = customtkinter.CTkEntry(frame_rolavel, width=10)
        nome, quantidade, preco = produto
        customtkinter.CTkLabel(frame_rolavel, text=nome).grid(row=i+1, column=0, padx=10, pady=5, sticky="ew")
        quantidade_atualizar.grid(row=i+1, column=1, padx=0, pady=5, sticky="ew")
        customtkinter.CTkLabel(frame_rolavel, text=preco).grid(row=i+1, column=2, padx=10, pady=5, sticky="ew")

        atualizar_btn = customtkinter.CTkButton(frame_rolavel, text="Atualizar Tabela", command= exibir_tabela);
        atualizar_btn.grid(row=i+2, column='1');

    # Configurar a grade para que as colunas se expandam igualmente
    for i in range(3):
        janela_gerenciar.grid_columnconfigure(i, weight=1)

def avisos():
    # Limpar qualquer widget existente no frame de avisos
    for widget in avisos_frame.winfo_children():
        widget.destroy()

    cursor.execute('''SELECT quantidade FROM produtos''')
    quantidades = cursor.fetchall()

    # Adicionar aviso para cada produto com quantidade abaixo do limite
    for quantidade in quantidades:
        if quantidade[0] < 5:
            aviso_quantidade = customtkinter.CTkLabel(
                avisos_frame,
                text="O produto está com perigo de ruptura. Quantidade disponível: {}".format(quantidade[0]),
                font=("Arial", 10)
            )
            aviso_quantidade.pack(pady=5, padx=10, anchor='w')

    if not quantidades:
        no_aviso = customtkinter.CTkLabel(
            avisos_frame,
            text="Todos os produtos estão com quantidade adequada.",
            font=("Arial", 10),
            fg_color="green"  # Alterar a cor do texto para destacar
        )
        no_aviso.pack(pady=5, padx=10, anchor='w')



def janela_de_gerenciamento():
    global janela_gerenciar;
    global frame_rolavel;

    janela_gerenciar = customtkinter.CTk()
    janela_gerenciar.geometry("850x550+400+200")
    janela_gerenciar.title('Stocksync')
    janela_gerenciar.after(201, lambda: janela_gerenciar.iconbitmap(os.path.join(os.path.dirname(__file__), 'images/stock_icon.ico')))

    # Frame com barra de rolagem
    frame_rolavel = customtkinter.CTkScrollableFrame(janela_gerenciar)
    frame_rolavel.pack(padx=10, pady=10, fill="both", expand=True)

    # Adiciona conteúdo ao frame rolável
    exibir_tabela()

    janela_gerenciar.mainloop()

#pagina de cadastro
def cad_produtos(tabc_func):
    global entry_nome_produto,entry_preco_produto,frame2_cad;
    
    
    cadastro_titulo= customtkinter.CTkLabel(tabc_func, text="Cadastrar Produtos");
    cadastro_titulo.pack();

    #frame para dividir a pagina em dois 
    frame1_cad = customtkinter.CTkFrame(master = tabc_func, width=820,height=550);
    frame1_cad.place(x=0,y=30);
    frame2_cad = customtkinter.CTkFrame(master = tabc_func, width=820,height=550);
    frame2_cad.place(x=425,y=30);

    #formulario para cadastro dos produtos FRAME !
    entry_nome_produto = customtkinter.CTkEntry(frame1_cad, width=400,height=39, placeholder_text="nome produto");
    entry_nome_produto.pack(pady=(85,15), padx=25);

    entry_preco_produto = customtkinter.CTkEntry(frame1_cad, width=400,height=39, placeholder_text="preco produto");
    entry_preco_produto.pack(pady=15, padx=25);
    
    menu_btn = customtkinter.CTkButton(frame1_cad,text="Cadastrar produto", command=cadastrar_produtos_banco);
    menu_btn.pack();
    #FRAME 2
    
    btn_atualizar_tabela = customtkinter.CTkButton(frame2_cad,text="Produtos cadastrados", command=produtos_mostrar);
    btn_atualizar_tabela.pack(padx= 110, pady=50);

#mostrar na tabela 
def produtos_mostrar():
    cursor.execute('''SELECT nome,quantidade,preco FROM produtos''');
    all_produtos = cursor.fetchall();

    for widget in frame2_cad.winfo_children():
        widget.destroy()

    for produto in all_produtos:
       nome,quantidade,preco = produto;
       all_produtos_msg = (f'Nome: {nome} Quantidade: {quantidade}  preço:{preco}');
       produtos_listar =customtkinter.CTkLabel(frame2_cad,text=all_produtos_msg);
       produtos_listar.pack(padx=50, pady=10);
    
    botao_mostrar = customtkinter.CTkButton(frame2_cad, text="Mostrar Produtos", command=produtos_mostrar)
    botao_mostrar.pack(pady=20)

#janela inicial
def janela_principal():
    global entry_login_senha;
    global entry_login_nome;
    global janela;
    global fail_login;

    fail_login = None;
    janela = customtkinter.CTk();
    janela.geometry("850x550+400+200");
    janela.title('Stocksync');
    janela.after(201, lambda: janela.iconbitmap(os.path.join(os.path.dirname(__file__), 'images/stock_icon.ico')))


    fonte_titulo_stocksync = customtkinter.CTkFont(family="Arial", size=30, weight="bold")
    inicio_texto =customtkinter.CTkLabel(janela,text="StockSync", font=fonte_titulo_stocksync);
    inicio_texto.pack(padx=10, pady=15);
    #fonte do texto de nome
    fonte_login_nome = customtkinter.CTkFont(family="Arial", size=17, weight="bold")
    texto_entry_nome = customtkinter.CTkLabel(janela,text="Nome: ", font=fonte_login_nome);
    texto_entry_nome.pack(padx=10,pady=15);
    # entrada nome
    entry_login_nome = customtkinter.CTkEntry(janela, width=400,height=39, placeholder_text="Usuário");
    entry_login_nome.pack(padx=10,pady=2);
    #fonte senha
    fonte_login_senha = customtkinter.CTkFont(family="Arial", size=17, weight="bold")
    texto_entry_senha =customtkinter.CTkLabel(janela,text="Senha: ", font=fonte_login_senha);
    texto_entry_senha.pack(padx=10,pady=10);

    #campo de entrada do login
    entry_login_senha = customtkinter.CTkEntry(janela,width=390,height=35, placeholder_text="Sua senha aqui",show="*");
    entry_login_senha.pack(padx=10,pady=15);

    btn_login = customtkinter.CTkButton(janela,width=100, height= 40,text="logar", command=login);
    btn_login.pack(padx=10,pady=20);

 
    janela.mainloop();

#cadastro no banco
def cadastrar_produtos_banco():
    nome_produto = entry_nome_produto.get();
    preco_produto = entry_preco_produto.get();

    quantidade = 0;
    situacao = 1;
   
    if preco_produto!= "" and nome_produto!="":
        preco_ofc = float(preco_produto);
        insert_produtos_banco = cursor.execute('''INSERT INTO produtos(nome,preco,situacao,quantidade) values(?,?,?,?)''',(nome_produto,preco_ofc,situacao,quantidade));
        conexao.commit();
    elif preco_produto == "" or nome_produto == "":
        messagebox.showwarning('Atenção','Digite algo nos campos de nome de produto e preco!');  

#ordem de execucao quando roda o app
def main():
    janela_principal();

if __name__=="__main__":
    main();
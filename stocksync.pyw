import customtkinter;
import sqlite3;
from tkinter import messagebox;
'''COISAS PARA FAZER 
    Fazer a pagina home
    fazer a pagina de gerenciamento 
    
'''
customtkinter.set_appearance_mode("dark");
customtkinter.set_default_color_theme('dark-blue');

conexao = sqlite3.connect('stocksync.db');
cursor = conexao.cursor();

#funcao que executa o  login
def login():
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
    menu_btn = customtkinter.CTkButton(tabh_func,text="Menu");
    menu_btn.pack();

def gerenciamento(tabg_func):
    menu_btn = customtkinter.CTkButton(tabg_func,text="Gerenciamento");
    menu_btn.pack();

def cad_produtos(tabc_func):
    global entry_codigo_produto,entry_nome_produto,entry_preco_produto;
    #frame para dividir a pagina em dois 
    frame1_cad = customtkinter.CTkFrame(master = tabc_func, width=850,height=550);
    frame1_cad.place(x=0,y=0);
    frame2_cad = customtkinter.CTkFrame(master = tabc_func, width=850,height=550);
    frame2_cad.place(x=425,y=0);

    #formulario para cadastro dos produtos
    entry_nome_produto = customtkinter.CTkEntry(frame1_cad, width=400,height=39, placeholder_text="nome produto");
    entry_nome_produto.pack(pady=(50,15), padx=15);

    entry_codigo_produto = customtkinter.CTkEntry(frame1_cad, width=400,height=39, placeholder_text="codigo do produto");
    entry_codigo_produto.pack(pady=15, padx=15);

    entry_preco_produto = customtkinter.CTkEntry(frame1_cad, width=400,height=39, placeholder_text="preco produto");
    entry_preco_produto.pack(pady=15, padx=15);
    
    menu_btn = customtkinter.CTkButton(frame1_cad,text="Cadastrar produto", command=cadastrar_produtos_banco);
    menu_btn.pack();
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
    janela.after(201, lambda :janela.iconbitmap('stock_icon.ico'));



    inicio_texto =customtkinter.CTkLabel(janela,text="Stock Sync");
    inicio_texto.pack(padx=10, pady=15);

    texto_entry_nome = customtkinter.CTkLabel(janela,text="Nome ");
    texto_entry_nome.pack(padx=10,pady=15);
    # entrada nome
    entry_login_nome = customtkinter.CTkEntry(janela, width=400,height=39, placeholder_text="Usuário");
    entry_login_nome.pack(padx=10,pady=2);

    #entrada senha
    texto_entry_senha =customtkinter.CTkLabel(janela,text="Senha");
    texto_entry_senha.pack(padx=10,pady=2);

    entry_login_senha = customtkinter.CTkEntry(janela,width=390,height=35, placeholder_text="Sua senha aqui",show="*");
    entry_login_senha.pack(padx=10,pady=15);

    btn_login = customtkinter.CTkButton(janela,width=100, height= 40,text="logar", command=login);
    btn_login.pack(padx=10,pady=20);
    
   
 
    janela.mainloop();

def cadastrar_produtos_banco():
   nome_produto = entry_nome_produto.get();
   preco_produto = 10.0;
   situacao = 1;
   quantidade = 0;
   codigo_produto = entry_codigo_produto.get();
   insert_produtos_banco = cursor.execute('''INSERT INTO produtos(nome,preco,situacao,quantidade) values(?,?,?,?)''',(nome_produto,codigo_produto,preco_produto,situacao,quantidade));
   conexao.commit();

#ordem de execucao quando roda o app
def main():
    janela_principal();

if __name__=="__main__":
    main();
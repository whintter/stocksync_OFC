import customtkinter;
import sqlite3;
from tkinter import messagebox;

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
    menu.geometry("850x550+530+220");
    
    #tabs
    tabview = customtkinter.CTkTabview(menu, width=850, height=550);
    tabview.pack();
    tabview.add("Home");
    tabview.add("Cadastrar Produtos");
    tabview.add("Gerenciamento");
    tabview.tab("Home").grid_columnconfigure(0,weight=1);
    tabview.tab("Cadastrar Produtos").grid_columnconfigure(0,weight=2);
    tabview.tab("Gerenciamento").grid_columnconfigure(0,weight=3);

   
    msg_menu = customtkinter.CTkLabel(menu, text='Bem Vindo a StockSync');
    msg_menu.pack(padx=10,pady=10);

    
    menu.mainloop();

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

#ordem de execucao quando roda o app
def main():
    janela_principal();

if __name__=="__main__":
    main();
import customtkinter as ctk 
from tkinter import *
import sqlite3
from tkinter import messagebox

class BackEnd():  
    def conecta_db(self):
        self.conn = sqlite3.connect("lake.db")
        self.cursor = self.conn.cursor()
        print("conect in db sucess!")

    def desconect_db(self):
        self.conn.close()
        print("desconet db!")

    def cria_table(self):
        self.conecta_db()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tb_users (
            Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            Username TEXT NOT NULL,
            Email TEXT NOT NULL,
            Password TEXT NOT NULL,
            ConfPassword TEXT NOT NULL
             );
         """)
        self.conn.commit()
        print("connect sucess!")
        self.desconect_db()

    def cadastrar_user(self):
        self.username_cadastro = self.username_cadastro_entry.get()
        self.email_cadastro = self.email_cadastro_entry.get() 
        self.senha_cadastro = self.password_cadastro_entry.get()
        self.rep_senha_cadastro = self.conf_pass_cadastro_entry.get()
    
        self.conecta_db()

        self.cursor.execute("""
            INSERT INTO tb_users(Username, Email, Password,ConfPassword)
            VALUES(?, ?, ?, ?)""",(self.username_cadastro,
                                    self.email_cadastro,
                                    self.senha_cadastro, 
                                    self.rep_senha_cadastro))
        try:
            if (self.username_cadastro == "" or self.email_cadastro =="" or self.senha_cadastro == "" or self.rep_senha_cadastro == ""):
                messagebox.showerror(title="Sistema Cadastro", message="ERRO!!!\nPreencher todos os campos!")
            elif(len(self.username_cadastro)< 4):
                messagebox.showwarning(title="Sistema Info", message="O nome deve ter mais de 4 letras")
            elif(len(self.senha_cadastro)< 4):
                messagebox.showwarning(title="Sistema Info", message="Senha deve ter mais de 4 letras")
            elif(self.senha_cadastro != self.rep_senha_cadastro):
                messagebox.showerror(title="Sistema Info", message="Erro senhas Diferentes!")
            else:
                self.conn.commit()
                messagebox.showinfo(title="sistema de login", message="Cadastrado com Sucesso!")
                self.desconect_db()
                self.limpa_entry_cadastro()
        
        except:
            messagebox.showerror(title="sitem info", message="Erro tente novamente mais tarde!")
            self.desconect_db()
    
    def log_valida(self):
        self.user_log = self.username_login_entry.get()
        self.senha_log = self.password_login_entry.get()
        #print(self.user_log, self.senha_log)
        #self.limpa_entry_login()
        self.conecta_db()

        self.cursor.execute("""SELECT * FROM tb_users WHERE(Username = ? AND Password =?)""", (self.user_log, self.senha_log))

        self.log_valida = self.cursor.fetchone()# percorre a tabela

        try:
            if(self.user_log == "" or self.senha_log ==""):
                messagebox.showwarning(title="Sistem Info", message="Preencha todos os campos!")
            elif (self.user_log in self.log_valida and self.senha_log in self.log_valida):
                messagebox.showinfo(title="Sistem Log", message=f"Bem Vindo {self.user_log} !!")
                self.desconect_db()
                self.limpa_entry_login()
        except:
            messagebox.showerror(title="Sistem ERRO", message="User Não Existe!")
            self.desconect_db()


class App(ctk.CTk, BackEnd):
    def __init__(self) -> None:
        super().__init__()
        self.tela()
        self.tela_log()

        
        
           

    def tela(self):
        self.geometry("700x400")
        self.title("create by valdiran")
        self.iconbitmap("ico.ico")
        self.resizable(False, False)
    
 
    def tela_log(self):
        self.img = PhotoImage(file="imo.png")
        self.lb_img = ctk.CTkLabel(self, image=self.img, text=None)
        self.lb_img.grid(row=1, column=0, padx=10, pady=75)
       
        self.title = ctk.CTkLabel(self, text="Sistema de Cadastro",font=("Roboto", 20), text_color="#00B0F0")
        self.title.grid(row=0, column=0, padx=15, pady=10)

        #criar frame
        self.frame_log = ctk.CTkFrame(self, width=350, height=380)
        self.frame_log.place(x=350, y=10)

        #colocando widgets in forms
        self.lb_title = ctk.CTkLabel(self.frame_log, text="Faça seu Login", font=("Roboto", 15))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)
        
        self.username_login_entry = ctk.CTkEntry(self.frame_log, width=300, placeholder_text="Seu ID", font=("Roboto", 16),corner_radius=20)
        self.username_login_entry.grid(row=1, column=0, padx=10, pady=10 )

        self.password_login_entry = ctk.CTkEntry(self.frame_log, width=300, placeholder_text="Sua senha", font=("Roboto", 16),show="*", corner_radius=20)
        self.password_login_entry.grid(row=2, column=0, padx=10, pady=10 )
       
        self.ver_senha= ctk.CTkCheckBox(self.frame_log, text="clique para ver senha", font=("Roboto", 12))
        self.ver_senha.grid(row=3, column=0, padx=10, pady=10 )

        self.btn_login = ctk.CTkButton(self.frame_log, width=300, text="Fazer Login", font=("Roboto", 16),corner_radius=15, command=self.log_valida)
        self.btn_login.grid(row=4, column=0, padx=10, pady=10 )

        self.sap = ctk.CTkLabel(self.frame_log, text="Crie seu Cadastro",font=("Roboto", 12), corner_radius=15)
        self.sap.grid(row=5, column=0, padx=10, pady=10 )

        self.btn_cad = ctk.CTkButton(self.frame_log, width=300, fg_color="green",
                                        hover_color="#050" ,text="Cadastre-Se",
                                        font=("Roboto", 16), corner_radius=15, command=self.tela_cadastro)
                                        
        self.btn_cad.grid(row=6, column=0, padx=10, pady=10 )

    
    def tela_cadastro(self):
        self.frame_log.place_forget()

        #criar frame
        self.frame_cad = ctk.CTkFrame(self, width=350, height=380)
        self.frame_cad.place(x=350, y=10)

        self.lb_title = ctk.CTkLabel(self.frame_log, text="Cadastro",text_color="#00B0F0", font=("Roboto", 20))
        self.lb_title.grid(row=0, column=0, padx=15, pady=10)



        #wigths cadastro
        self.username_cadastro_entry = ctk.CTkEntry(self.frame_cad, width=300, placeholder_text="Seu nome", font=("Roboto", 16),corner_radius=20)
        self.username_cadastro_entry.grid(row=1, column=0, padx=10, pady=10 )

        self.email_cadastro_entry = ctk.CTkEntry(self.frame_cad, width=300, placeholder_text="Seu E-mail", font=("Roboto", 16), corner_radius=20)
        self.email_cadastro_entry.grid(row=2, column=0, padx=10, pady=10 )

        self.password_cadastro_entry = ctk.CTkEntry(self.frame_cad, width=300, placeholder_text="Sua senha", font=("Roboto", 16),show="*",corner_radius=20)
        self.password_cadastro_entry.grid(row=3, column=0, padx=10, pady=10 )

        self.conf_pass_cadastro_entry = ctk.CTkEntry(self.frame_cad, width=300, placeholder_text="confirme a senha", font=("Roboto", 16),show="*", corner_radius=20)
        self.conf_pass_cadastro_entry.grid(row=4, column=0, padx=10, pady=10 )

        self.ver_senha= ctk.CTkCheckBox(self.frame_cad, text="clique para ver senha", font=("Roboto", 12))
        self.ver_senha.grid(row=5, column=0, padx=10, pady=10 )

        self.btn_cadastrar_user = ctk.CTkButton(self.frame_cad, width=300, fg_color="green",
                                        hover_color="#050" ,text="Cadastrar",
                                        font=("Roboto", 16), corner_radius=15, command=self.cadastrar_user)
                                        
        self.btn_cadastrar_user.grid(row=6, column=0, padx=10, pady=10 )

        self.btn_login_back = ctk.CTkButton(self.frame_cad, width=300, text="Voltar",fg_color="#444", hover_color="#333" ,font=("Roboto", 16),command=self.tela_log, corner_radius=15)
        self.btn_login_back.grid(row=7, column=0, padx=10, pady=10 )

    def limpa_entry_cadastro(self):
        self.username_cadastro_entry.delete(0, END)
        self.email_cadastro_entry.delete(0, END)
        self.password_cadastro_entry.delete(0, END)
        self.conf_pass_cadastro_entry.delete(0, END)
    
    def limpa_entry_login(self):
        self.username_login_entry.delete(0,END)
        self.password_login_entry.delete(0, END)
     

if __name__ == "__main__":
    bk = BackEnd()
    app = App()
    app.mainloop()
    
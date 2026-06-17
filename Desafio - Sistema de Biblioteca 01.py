import sqlite3
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta

# CONFIGURAÇÕES
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# BANCO DE DADOS
conexao = sqlite3.connect("biblioteca.db")
cursor = conexao.cursor()

# TABELA LIVROS
cursor.execute("""
CREATE TABLE IF NOT EXISTS livros(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    genero TEXT NOT NULL,
    paginas INTEGER NOT NULL,
    quantidade INTEGER NOT NULL
)
""")

# TABELA USUÁRIOS
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT NOT NULL UNIQUE,
    telefone TEXT NOT NULL,
    email TEXT NOT NULL
)
""")

# TABELA DE EMPRÉSTIMOS
cursor.execute("""
CREATE TABLE IF NOT EXISTS emprestimos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    livro_id INTEGER NOT NULL,
    data_emprestimo TEXT NOT NULL,
    data_devolucao TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Emprestado',
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (livro_id) REFERENCES livros(id)
)
""")

conexao.commit()

# CLASSE PRINCIPAL
class SistemaLivros:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Livros")
        self.root.geometry("500x500")
        titulo = ctk.CTkLabel(root,text="Sistema de Biblioteca", font=("Arial", 24, "bold"))
        titulo.pack(pady=30)

        btn_cadastrar = ctk.CTkButton(root,text="Cadastrar Livro", width=220, command=self.abrir_cadastro_livros)
        btn_cadastrar.pack(pady=10)

        btn_cadastrar = ctk.CTkButton(root,text="Cadastrar Usuário", width=220, command=self.abrir_cadastro_usuarios)
        btn_cadastrar.pack(pady=10)

        btn_cadastrar = ctk.CTkButton(root,text="Empréstimos", width=220, command=self.abrir_emprestimo)
        btn_cadastrar.pack(pady=10)

        btn_cadastrar = ctk.CTkButton(root,text="Consultar Empréstimos", width=220, command=self.abrir_consultar_emprestimos)
        btn_cadastrar.pack(pady=10)

        btn_listar = ctk.CTkButton( root, text="Listar Livros",  width=220, command=self.abrir_listagem_livros)
        btn_listar.pack(pady=10)

        btn_listar = ctk.CTkButton( root, text="Listar Usuários",  width=220, command=self.abrir_listagem_usuarios)
        btn_listar.pack(pady=10)

    # CADASTRO DE LIVROS
    def abrir_cadastro_livros(self):
        janela = ctk.CTkToplevel(self.root)
        janela.title("Cadastro de Livro")
        janela.geometry("500x400")
        janela.grab_set()
        ctk.CTkLabel(janela,text="Cadastrar Livro",font=("Arial", 20, "bold")).pack(pady=15)
        titulo = ctk.CTkEntry(janela, placeholder_text="Título")
        titulo.pack(pady=5, padx=20, fill="x")
        autor = ctk.CTkEntry(janela,placeholder_text="Autor")
        autor.pack(pady=5, padx=20, fill="x")
        genero = ctk.CTkEntry( janela,placeholder_text="Gênero")
        genero.pack(pady=5, padx=20, fill="x")
        paginas = ctk.CTkEntry(janela,placeholder_text="Número de Páginas")
        paginas.pack(pady=5, padx=20, fill="x")
        quantidade = ctk.CTkEntry(janela,placeholder_text="Quantidade")
        quantidade.pack(pady=5, padx=20, fill="x")

        def salvar():
            if (not titulo.get() or not autor.get()
                or not genero.get()or not paginas.get()):
                messagebox.showwarning("Atenção", "Preencha todos os campos!")
                return
            cursor.execute("""
            INSERT INTO livros
            (titulo, autor, genero, paginas, quantidade)
            VALUES (?, ?, ?, ?, ?)
            """, (titulo.get(),autor.get(), genero.get(), paginas.get(), quantidade.get()))
            conexao.commit()
            messagebox.showinfo("Sucesso","Livro cadastrado!")
            janela.destroy()
            
        ctk.CTkButton(janela,text="Salvar", command=salvar).pack(pady=20)
    
    # CADASTRO DE USUÁRIOS
    def abrir_cadastro_usuarios(self):
        janela = ctk.CTkToplevel(self.root)
        janela.title("Cadastro de Usuário")
        janela.geometry("500x400")
        janela.grab_set()
        ctk.CTkLabel(janela,text="Cadastrar Usuário",font=("Arial", 20, "bold")).pack(pady=15)
        nome = ctk.CTkEntry(janela, placeholder_text="Nome Completo")
        nome.pack(pady=5, padx=20, fill="x")
        cpf = ctk.CTkEntry(janela,placeholder_text="CPF")
        cpf.pack(pady=5, padx=20, fill="x")
        telefone = ctk.CTkEntry( janela,placeholder_text="Telefone")
        telefone.pack(pady=5, padx=20, fill="x")
        email = ctk.CTkEntry(janela,placeholder_text="Email")
        email.pack(pady=5, padx=20, fill="x")

        def salvar():
            if (not nome.get() or not cpf.get()
                or not telefone.get()or not email.get()):
                messagebox.showwarning("Atenção", "Preencha todos os campos!")
                return
            cursor.execute("""
            INSERT INTO usuarios
            (nome, cpf, telefone, email)
            VALUES (?, ?, ?, ?)
            """, (nome.get(),cpf.get(), telefone.get(), email.get()))
            conexao.commit()
            messagebox.showinfo("Sucesso","Usuário cadastrado!")
            janela.destroy()
            
        ctk.CTkButton(janela,text="Salvar", command=salvar).pack(pady=20)

    # EMPRÉSTIMO
    def abrir_emprestimo(self):
        janela = ctk.CTkToplevel(self.root)
        janela.title("Empréstimo de Livro")
        janela.geometry("500x400")
        janela.grab_set()
        ctk.CTkLabel(janela,text="Registrar Empréstimo",font=("Arial", 20, "bold")).pack(pady=15)

        # Carrega usuários
        cursor.execute("SELECT id, nome FROM usuarios ORDER BY nome")
        usuarios = cursor.fetchall()
        usuarios_dict = {u[1]: u[0] for u in usuarios}
        usuarios_nomes = list(usuarios_dict.keys()) if usuarios else ["Nenhum usuário"]

        # Carrega livros com quantidade > 0
        cursor.execute("SELECT id, titulo FROM livros WHERE quantidade > 0 ORDER BY titulo")
        livros = cursor.fetchall()
        livros_dict = {l[1]: l[0] for l in livros}
        livros_nomes = list(livros_dict.keys()) if livros else ["Nenhum livro disponível"]

        frame = ctk.CTkFrame(janela, fg_color="transparent")
        frame.pack(padx=30, fill="x")

        ctk.CTkLabel(frame, text="Usuário:").grid(row=0, column=0, sticky="w", pady=8)
        cb_usuario = ctk.CTkComboBox(frame, values=usuarios_nomes, width=340, state="readonly")
        cb_usuario.grid(row=0, column=1, padx=12, pady=8)
        if usuarios_nomes:
            cb_usuario.set(usuarios_nomes[0])

        ctk.CTkLabel(frame, text="Livro:").grid(row=1, column=0, sticky="w", pady=8)
        cb_livro = ctk.CTkComboBox(frame, values=livros_nomes, width=340, state="readonly")
        cb_livro.grid(row=1, column=1, padx=12, pady=8)
        if livros_nomes:
            cb_livro.set(livros_nomes[0])

        def emprestar():
            if not usuarios_nomes or not livros_nomes:
                messagebox.showwarning("Atenção", "Não há usuários ou livros disponíveis para empréstimo!")
                return
            usuario_id = usuarios_dict[cb_usuario.get()]
            livro_id = livros_dict[cb_livro.get()]
            data_emprestimo = datetime.now().strftime("%Y-%m-%d")
            data_devolucao = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

            cursor.execute("""
            INSERT INTO emprestimos
            (usuario_id, livro_id, data_emprestimo, data_devolucao)
            VALUES (?, ?, ?, ?)
            """, (usuario_id, livro_id, data_emprestimo, data_devolucao))
            
            cursor.execute("""
            UPDATE livros
            SET quantidade = quantidade - 1
            WHERE id=?
            """, (livro_id,))
            
            conexao.commit()
            messagebox.showinfo("Sucesso", f"Empréstimo registrado!\nDevolução prevista para {data_devolucao}")
            janela.destroy()

        ctk.CTkButton(janela, text="Registrar Empréstimo", width=220, command=emprestar).pack(pady=20)

    # CONSULTAR EMPRÉSTIMOS
    def abrir_consultar_emprestimos(self):
        janela = ctk.CTkToplevel(self.root)
        janela.title("Consultar Empréstimos")
        janela.geometry("500x400")
        janela.grab_set()
        ctk.CTkLabel(janela,text="Empréstimos Ativos",font=("Arial", 20, "bold")).pack(pady=15)

        frame_scroll = ctk.CTkScrollableFrame(janela)
        frame_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        cursor.execute("""
        SELECT u.nome, l.titulo, e.data_emprestimo, e.data_devolucao
        FROM emprestimos e
        JOIN usuarios u ON u.id = e.usuario_id
        JOIN livros l ON l.id = e.livro_id
        WHERE e.status='Emprestado'
        ORDER BY e.data_emprestimo DESC
        """)
        registros = cursor.fetchall()

        if not registros:
            ctk.CTkLabel(frame_scroll, text="Nenhum empréstimo ativo.",
                         font=("Arial", 14), text_color="gray").pack(pady=30)
            return

        for usuario, livro, emp, dev in registros:
            linha = ctk.CTkFrame(frame_scroll)
            linha.pack(fill="x", pady=2)
            ctk.CTkLabel(linha, text=usuario, width=150).grid(row=0, column=0, padx=5)
            ctk.CTkLabel(linha, text=livro, width=200).grid(row=0, column=1, padx=5)
            ctk.CTkLabel(linha, text=f"Empréstimo: {emp}", width=120).grid(row=0, column=2, padx=5)
            ctk.CTkLabel(linha, text=f"Devolução: {dev}", width=120).grid(row=0, column=3, padx=5)

    # LISTAGEM DE LIVROS
    def abrir_listagem_livros(self):
        janela = ctk.CTkToplevel(self.root)
        janela.title("Livros Cadastrados")
        janela.geometry("850x500")
        janela.grab_set()
        frame_scroll = ctk.CTkScrollableFrame(janela)
        frame_scroll.pack(fill="both",expand=True,padx=10,pady=10)

        def carregar_dados():
            for widget in frame_scroll.winfo_children():
                widget.destroy()
            cursor.execute("""
            SELECT * FROM livros
            ORDER BY id DESC
            """)
            registros = cursor.fetchall()
            cabecalho = ctk.CTkFrame(frame_scroll)
            cabecalho.pack(fill="x", pady=3)
            ctk.CTkLabel(cabecalho, text="Ações", width=180).grid(row=0, column=0)
            ctk.CTkLabel(cabecalho, text="Título",width=100).grid(row=0, column=2)
            ctk.CTkLabel(cabecalho, text="Autor", width=180).grid(row=0, column=3)
            ctk.CTkLabel(cabecalho, text="Gênero", width=120).grid(row=0, column=4)
            ctk.CTkLabel(cabecalho, text="Páginas", width=120).grid(row=0, column=5)            
            ctk.CTkLabel(cabecalho, text="Quantidade", width=200).grid(row=0, column=6)

            for registro in registros:
                id_livro = registro[0]
                linha = ctk.CTkFrame(frame_scroll)
                linha.pack(fill="x", pady=2)
                ctk.CTkLabel(linha, text=registro[1],justify='center', width=100).grid(row=0, column=2)
                ctk.CTkLabel(linha, text=registro[2],justify='center', width=180).grid(row=0, column=3)
                ctk.CTkLabel(linha, text=registro[3],justify='center', width=120).grid(row=0, column=4)
                ctk.CTkLabel(linha, text=registro[4],justify='center', width=120).grid(row=0, column=5)
                ctk.CTkLabel(linha, text=registro[5],justify='center', width=200).grid(row=0, column=6)

                btn_editar = ctk.CTkButton(linha, text="Alterar", width=70, command=lambda i=id_livro: self.alterar_livro( i,carregar_dados))
                btn_editar.grid(row=0, column=0, padx=5)
                btn_excluir = ctk.CTkButton(linha, text="Excluir", width=70, fg_color="red", hover_color="#aa0000", command=lambda i=id_livro:self.excluir_livro(i,carregar_dados))
                btn_excluir.grid(row=0,column=1,padx=5)

        carregar_dados()

    # ALTERAÇÃO DE LIVROS
    def alterar_livro(self, id_livro, atualizar_lista):
        cursor.execute("""
        SELECT * FROM livros
        WHERE id=?
        """, (id_livro,))
        livro = cursor.fetchone()
        janela = ctk.CTkToplevel(self.root)
        janela.title("Alterar Livro")
        janela.geometry("600x600")
        janela.grab_set()
        titulo = ctk.CTkEntry(janela)
        titulo.insert(0, livro[1])
        titulo.pack(pady=10, padx=20, fill="x")
        autor = ctk.CTkEntry(janela)
        autor.insert(0, livro[2])
        autor.pack(pady=10, padx=20, fill="x")
        genero = ctk.CTkEntry(janela)
        genero.insert(0, livro[3])
        genero.pack(pady=10, padx=20, fill="x")
        paginas = ctk.CTkEntry(janela)
        paginas.insert(0, livro[4])
        paginas.pack(pady=10, padx=20, fill="x")
        quantidade = ctk.CTkEntry(janela)
        quantidade.insert(0, livro[5])
        quantidade.pack(pady=10, padx=20, fill="x")
        
        def salvar():
            cursor.execute("""
            UPDATE livros
            SET titulo=?,
                autor=?,
                genero=?,
                paginas=?,
                quantidade=?
            WHERE id=?
            """,
            (titulo.get(), autor.get(), genero.get(), paginas.get(), quantidade.get(), id_livro))
            conexao.commit()

            messagebox.showinfo("Sucesso", "Registro atualizado!" )
            atualizar_lista()
            janela.destroy()

        ctk.CTkButton(janela, text="Salvar Alterações", command=salvar).pack(pady=20)


    # EXCLUIR LIVROS
    def excluir_livro(self, id_livro, atualizar_lista):
        resposta = messagebox.askyesno("Confirmar", "Deseja excluir este livro?")

        if resposta:
            cursor.execute("""
            DELETE FROM livros
            WHERE id=?
            """, (id_livro,))
            conexao.commit()
            atualizar_lista()
    
    # LISTAGEM DE USUÁRIOS
    def abrir_listagem_usuarios(self):
        janela = ctk.CTkToplevel(self.root)
        janela.title("Usuários Cadastrados")
        janela.geometry("700x500")
        janela.grab_set()
        frame_scroll = ctk.CTkScrollableFrame(janela)
        frame_scroll.pack(fill="both",expand=True,padx=10,pady=10)

        def carregar_dados():
            for widget in frame_scroll.winfo_children():
                widget.destroy()

            cursor.execute("SELECT * FROM usuarios ORDER BY id DESC")
            registros = cursor.fetchall()

            cabecalho = ctk.CTkFrame(frame_scroll)
            cabecalho.pack(fill="x", pady=3)
            ctk.CTkLabel(cabecalho, text="Ações", width=180).grid(row=0, column=0)
            ctk.CTkLabel(cabecalho, text="Nome",width=200).grid(row=0, column=2)
            ctk.CTkLabel(cabecalho, text="CPF", width=150).grid(row=0, column=3)
            ctk.CTkLabel(cabecalho, text="Telefone", width=150).grid(row=0, column=4)
            ctk.CTkLabel(cabecalho, text="Email", width=200).grid(row=0, column=5)

            for registro in registros:
                id_usuario = registro[0]
                linha = ctk.CTkFrame(frame_scroll)
                linha.pack(fill="x", pady=2)
                ctk.CTkLabel(linha, text=registro[1], width=200).grid(row=0, column=2)
                ctk.CTkLabel(linha, text=registro[2], width=150).grid(row=0, column=3)
                ctk.CTkLabel(linha, text=registro[3], width=150).grid(row=0, column=4)
                ctk.CTkLabel(linha, text=registro[4], width=200).grid(row=0, column=5)

                btn_editar = ctk.CTkButton(linha, text="Alterar", width=70, command=lambda i=id_usuario: self.alterar_usuario(i, carregar_dados))
                btn_editar.grid(row=0, column=0, padx=5)

                btn_excluir = ctk.CTkButton(linha, text="Excluir", width=70, fg_color="red", hover_color="#aa0000", command=lambda i=id_usuario: self.excluir_usuario(i, carregar_dados))
                btn_excluir.grid(row=0, column=1, padx=5)

        carregar_dados()
    
    # ALTERAÇÃO DE USUÁRIOS
    def alterar_usuario(self, id_usuario, atualizar_lista):
        cursor.execute("""
        SELECT * FROM usuarios
        WHERE id=?
        """, (id_usuario,))
        usuario = cursor.fetchone()
        janela = ctk.CTkToplevel(self.root)
        janela.title("Alterar Usuário")
        janela.geometry("600x500")
        janela.grab_set()
        nome = ctk.CTkEntry(janela)
        nome.insert(0, usuario[1])
        nome.pack(pady=10, padx=20, fill="x")
        cpf = ctk.CTkEntry(janela)
        cpf.insert(0, usuario[2])
        cpf.pack(pady=10, padx=20, fill="x")
        telefone = ctk.CTkEntry(janela)
        telefone.insert(0, usuario[3])
        telefone.pack(pady=10, padx=20, fill="x")
        email = ctk.CTkEntry(janela)
        email.insert(0, usuario[4])
        email.pack(pady=10, padx=20, fill="x")

        def salvar():
            cursor.execute("""
            UPDATE usuarios
            SET nome=?,
                cpf=?,
                telefone=?,
                email=?
            WHERE id=?
            """,
            (nome.get(), cpf.get(), telefone.get(), email.get(), id_usuario))
            conexao.commit()

            messagebox.showinfo("Sucesso", "Registro atualizado!" )
            atualizar_lista()
            janela.destroy()

        ctk.CTkButton(janela, text="Salvar Alterações", command=salvar).pack(pady=20)

    # EXCLUIR USUÁRIOS
    def excluir_usuario(self, id_usuario, atualizar_lista):
        resposta = messagebox.askyesno("Confirmar", "Deseja excluir este usuário?")

        if resposta:
            cursor.execute("""
            DELETE FROM usuarios
            WHERE id=?
            """, (id_usuario,))
            conexao.commit()
            atualizar_lista()

# EXECUTAR SISTEMA
root = ctk.CTk()
app = SistemaLivros(root)
root.mainloop()
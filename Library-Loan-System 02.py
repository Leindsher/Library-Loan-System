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

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT NOT NULL UNIQUE,
    telefone TEXT NOT NULL,
    email TEXT NOT NULL
)
""")

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


# FUNÇÕES AUXILIARES
def centralizar(janela, largura, altura):
    janela.update_idletasks()
    x = (janela.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela.winfo_screenheight() // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")


def campo(parent, label, row, placeholder=""):
    ctk.CTkLabel(parent, text=label, font=("Segoe UI", 13)).grid(
        row=row, column=0, sticky="w", padx=20, pady=(10, 2))
    entry = ctk.CTkEntry(parent, width=320, placeholder_text=placeholder,
                         font=("Segoe UI", 13))
    entry.grid(row=row, column=1, padx=20, pady=(10, 2))
    return entry


# MODAL: CADASTRO DE LIVROS
def abrir_cadastro_livros(master):
    modal = ctk.CTkToplevel(master)
    modal.title("Cadastrar Livro")
    modal.resizable(False, False)
    centralizar(modal, 560, 440)
    modal.grab_set()

    ctk.CTkLabel(modal, text="Cadastro de Livro",
                 font=("Segoe UI", 18, "bold")).grid(
        row=0, column=0, columnspan=2, pady=(20, 10))

    e_titulo   = campo(modal, "Título",     1, "Ex: Dom Casmurro")
    e_autor    = campo(modal, "Autor",      2, "Ex: Machado de Assis")
    e_genero   = campo(modal, "Gênero",     3, "Ex: Romance")
    e_paginas  = campo(modal, "Páginas",    4, "Ex: 256")
    e_qtd      = campo(modal, "Quantidade", 5, "Ex: 3")

    def salvar():
        titulo    = e_titulo.get().strip()
        autor     = e_autor.get().strip()
        genero    = e_genero.get().strip()
        paginas   = e_paginas.get().strip()
        qtd       = e_qtd.get().strip()

        if not all([titulo, autor, genero, paginas, qtd]):
            messagebox.showwarning("Atenção", "Preencha todos os campos.", parent=modal)
            return
        if not paginas.isdigit() or not qtd.isdigit():
            messagebox.showwarning("Atenção", "Páginas e Quantidade devem ser números inteiros.", parent=modal)
            return

        cursor.execute(
            "INSERT INTO livros (titulo, autor, genero, paginas, quantidade) VALUES (?,?,?,?,?)",
            (titulo, autor, genero, int(paginas), int(qtd))
        )
        conexao.commit()
        messagebox.showinfo("Sucesso", f'Livro "{titulo}" cadastrado!', parent=modal)
        modal.destroy()

    ctk.CTkButton(modal, text="Salvar", width=180, height=38,
                  font=("Segoe UI", 13, "bold"), command=salvar).grid(
        row=6, column=0, columnspan=2, pady=24)


# MODAL: CADASTRO DE USUÁRIOS 
def abrir_cadastro_usuarios(master):
    modal = ctk.CTkToplevel(master)
    modal.title("Cadastrar Usuário")
    modal.resizable(False, False)
    centralizar(modal, 560, 400)
    modal.grab_set()

    ctk.CTkLabel(modal, text="Cadastro de Usuário",
                 font=("Segoe UI", 18, "bold")).grid(
        row=0, column=0, columnspan=2, pady=(20, 10))

    e_nome      = campo(modal, "Nome",      1, "Nome completo")
    e_cpf       = campo(modal, "CPF",       2, "000.000.000-00")
    e_telefone  = campo(modal, "Telefone",  3, "(00) 00000-0000")
    e_email     = campo(modal, "E-mail",    4, "usuario@email.com")

    def salvar():
        nome     = e_nome.get().strip()
        cpf      = e_cpf.get().strip()
        telefone = e_telefone.get().strip()
        email    = e_email.get().strip()

        if not all([nome, cpf, telefone, email]):
            messagebox.showwarning("Atenção", "Preencha todos os campos.", parent=modal)
            return

        try:
            cursor.execute(
                "INSERT INTO usuarios (nome, cpf, telefone, email) VALUES (?,?,?,?)",
                (nome, cpf, telefone, email)
            )
            conexao.commit()
            messagebox.showinfo("Sucesso", f'Usuário "{nome}" cadastrado!', parent=modal)
            modal.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "CPF já cadastrado.", parent=modal)

    ctk.CTkButton(modal, text="Salvar", width=180, height=38,
                  font=("Segoe UI", 13, "bold"), command=salvar).grid(
        row=5, column=0, columnspan=2, pady=24)


# MODAL: EMPRÉSTIMO 
def abrir_emprestimo(master):
    modal = ctk.CTkToplevel(master)
    modal.title("Registrar Empréstimo")
    modal.resizable(False, False)
    centralizar(modal, 560, 340)
    modal.grab_set()

    ctk.CTkLabel(modal, text="Registrar Empréstimo",
                 font=("Segoe UI", 18, "bold")).pack(pady=(20, 16))

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

    frame = ctk.CTkFrame(modal, fg_color="transparent")
    frame.pack(padx=30, fill="x")

    ctk.CTkLabel(frame, text="Usuário:", font=("Segoe UI", 13)).grid(
        row=0, column=0, sticky="w", pady=8)
    cb_usuario = ctk.CTkComboBox(frame, values=usuarios_nomes, width=340,
                                 font=("Segoe UI", 13), state="readonly")
    cb_usuario.grid(row=0, column=1, padx=12, pady=8)
    if usuarios_nomes:
        cb_usuario.set(usuarios_nomes[0])

    ctk.CTkLabel(frame, text="Livro:", font=("Segoe UI", 13)).grid(
        row=1, column=0, sticky="w", pady=8)
    cb_livro = ctk.CTkComboBox(frame, values=livros_nomes, width=340,
                                font=("Segoe UI", 13), state="readonly")
    cb_livro.grid(row=1, column=1, padx=12, pady=8)
    if livros_nomes:
        cb_livro.set(livros_nomes[0])

    def emprestar():
        nome_usuario = cb_usuario.get()
        nome_livro   = cb_livro.get()

        if nome_usuario not in usuarios_dict:
            messagebox.showwarning("Atenção", "Selecione um usuário válido.", parent=modal)
            return
        if nome_livro not in livros_dict:
            messagebox.showwarning("Atenção", "Selecione um livro válido.", parent=modal)
            return

        usuario_id = usuarios_dict[nome_usuario]
        livro_id   = livros_dict[nome_livro]
        hoje       = datetime.today()
        devolucao  = hoje + timedelta(days=7)

        cursor.execute(
            "INSERT INTO emprestimos (usuario_id, livro_id, data_emprestimo, data_devolucao, status) VALUES (?,?,?,?,?)",
            (usuario_id, livro_id,
             hoje.strftime("%d/%m/%Y"),
             devolucao.strftime("%d/%m/%Y"),
             "Emprestado")
        )
        cursor.execute("UPDATE livros SET quantidade = quantidade - 1 WHERE id = ?", (livro_id,))
        conexao.commit()

        messagebox.showinfo(
            "Sucesso",
            f'Livro "{nome_livro}" emprestado para {nome_usuario}.\nDevolução: {devolucao.strftime("%d/%m/%Y")}',
            parent=modal
        )
        modal.destroy()

    ctk.CTkButton(modal, text="Emprestar", width=200, height=38,
                  font=("Segoe UI", 13, "bold"), command=emprestar).pack(pady=20)


# MODAL: LIVROS EMPRESTADOS 
def abrir_emprestados(master):
    modal = ctk.CTkToplevel(master)
    modal.title("Livros Emprestados")
    modal.resizable(False, False)
    centralizar(modal, 860, 500)
    modal.grab_set()

    ctk.CTkLabel(modal, text="Livros Emprestados",
                 font=("Segoe UI", 18, "bold")).pack(pady=(20, 12))

    # Frame de cabeçalho
    header = ctk.CTkFrame(modal, fg_color="#1a73e8", corner_radius=8)
    header.pack(padx=20, fill="x")

    colunas = ["Usuário", "Livro", "Data Empréstimo", "Data Devolução", "Status"]
    larguras = [180, 220, 140, 140, 110]
    for i, (col, larg) in enumerate(zip(colunas, larguras)):
        ctk.CTkLabel(header, text=col, width=larg,
                     font=("Segoe UI", 12, "bold"),
                     text_color="white").grid(row=0, column=i, padx=4, pady=8)

    # Área rolável
    scroll = ctk.CTkScrollableFrame(modal, height=340)
    scroll.pack(padx=20, pady=(4, 16), fill="both", expand=True)

    cursor.execute("""
        SELECT u.nome, l.titulo, e.data_emprestimo, e.data_devolucao, e.status
        FROM emprestimos e
        JOIN usuarios u ON u.id = e.usuario_id
        JOIN livros l ON l.id = e.livro_id
        ORDER BY e.id DESC
    """)
    registros = cursor.fetchall()

    if not registros:
        ctk.CTkLabel(scroll, text="Nenhum empréstimo registrado.",
                     font=("Segoe UI", 13), text_color="gray").pack(pady=30)
    else:
        for idx, (usuario, livro, emp, dev, status) in enumerate(registros):
            bg = "#f0f4ff" if idx % 2 == 0 else "#ffffff"
            linha = ctk.CTkFrame(scroll, fg_color=bg, corner_radius=6)
            linha.pack(fill="x", pady=2)

            valores = [usuario, livro, emp, dev]
            for i, (val, larg) in enumerate(zip(valores, larguras)):
                ctk.CTkLabel(linha, text=val, width=larg,
                             font=("Segoe UI", 12), anchor="center").grid(
                    row=0, column=i, padx=4, pady=8)

            # Badge de status
            cor_badge = "#2ecc71" if status == "Devolvido" else "#e67e22"
            badge = ctk.CTkFrame(linha, fg_color=cor_badge, corner_radius=10, width=90, height=26)
            badge.grid(row=0, column=4, padx=8, pady=8)
            badge.grid_propagate(False)
            ctk.CTkLabel(badge, text=status, font=("Segoe UI", 11, "bold"),
                         text_color="white").place(relx=0.5, rely=0.5, anchor="center")


# MODAL: LISTAGEM DE LIVROS (com Alterar/Excluir)
def abrir_listagem_livros(master):
    modal = ctk.CTkToplevel(master)
    modal.title("Livros Cadastrados")
    modal.resizable(False, False)
    centralizar(modal, 900, 520)
    modal.grab_set()

    ctk.CTkLabel(modal, text="Livros Cadastrados",
                 font=("Segoe UI", 18, "bold")).pack(pady=(20, 12))

    header = ctk.CTkFrame(modal, fg_color="#1a73e8", corner_radius=8)
    header.pack(padx=20, fill="x")

    colunas = ["Título", "Autor", "Gênero", "Páginas", "Quantidade", "Ações"]
    larguras = [180, 160, 110, 80, 100, 160]
    for i, (col, larg) in enumerate(zip(colunas, larguras)):
        ctk.CTkLabel(header, text=col, width=larg,
                     font=("Segoe UI", 12, "bold"),
                     text_color="white").grid(row=0, column=i, padx=4, pady=8)

    scroll = ctk.CTkScrollableFrame(modal, height=340)
    scroll.pack(padx=20, pady=(4, 16), fill="both", expand=True)

    def carregar_dados():
        for widget in scroll.winfo_children():
            widget.destroy()

        cursor.execute("SELECT * FROM livros ORDER BY id DESC")
        registros = cursor.fetchall()

        if not registros:
            ctk.CTkLabel(scroll, text="Nenhum livro cadastrado.",
                         font=("Segoe UI", 13), text_color="gray").pack(pady=30)
            return

        for idx, registro in enumerate(registros):
            id_livro, titulo, autor, genero, paginas, quantidade = registro
            bg = "#f0f4ff" if idx % 2 == 0 else "#ffffff"
            linha = ctk.CTkFrame(scroll, fg_color=bg, corner_radius=6)
            linha.pack(fill="x", pady=2)

            valores = [titulo, autor, genero, paginas, quantidade]
            for i, (val, larg) in enumerate(zip(valores, larguras)):
                ctk.CTkLabel(linha, text=val, width=larg,
                             font=("Segoe UI", 12), anchor="center").grid(
                    row=0, column=i, padx=4, pady=8)

            acoes = ctk.CTkFrame(linha, fg_color="transparent")
            acoes.grid(row=0, column=5, padx=4, pady=4)

            ctk.CTkButton(acoes, text="Alterar", width=70, height=28,
                          font=("Segoe UI", 11),
                          command=lambda i=id_livro: alterar_livro(modal, i, carregar_dados)
                          ).grid(row=0, column=0, padx=3)

            ctk.CTkButton(acoes, text="Excluir", width=70, height=28,
                          font=("Segoe UI", 11), fg_color="#e74c3c", hover_color="#c0392b",
                          command=lambda i=id_livro: excluir_livro(modal, i, carregar_dados)
                          ).grid(row=0, column=1, padx=3)

    carregar_dados()


# MODAL: ALTERAR LIVRO
def alterar_livro(master, id_livro, atualizar_lista):
    cursor.execute("SELECT * FROM livros WHERE id=?", (id_livro,))
    livro = cursor.fetchone()
    if not livro:
        return

    modal = ctk.CTkToplevel(master)
    modal.title("Alterar Livro")
    modal.resizable(False, False)
    centralizar(modal, 560, 440)
    modal.grab_set()

    ctk.CTkLabel(modal, text="Alterar Livro",
                 font=("Segoe UI", 18, "bold")).grid(
        row=0, column=0, columnspan=2, pady=(20, 10))

    e_titulo  = campo(modal, "Título", 1)
    e_titulo.insert(0, livro[1])
    e_autor   = campo(modal, "Autor", 2)
    e_autor.insert(0, livro[2])
    e_genero  = campo(modal, "Gênero", 3)
    e_genero.insert(0, livro[3])
    e_paginas = campo(modal, "Páginas", 4)
    e_paginas.insert(0, str(livro[4]))
    e_qtd     = campo(modal, "Quantidade", 5)
    e_qtd.insert(0, str(livro[5]))

    def salvar():
        titulo  = e_titulo.get().strip()
        autor   = e_autor.get().strip()
        genero  = e_genero.get().strip()
        paginas = e_paginas.get().strip()
        qtd     = e_qtd.get().strip()

        if not all([titulo, autor, genero, paginas, qtd]):
            messagebox.showwarning("Atenção", "Preencha todos os campos.", parent=modal)
            return
        if not paginas.isdigit() or not qtd.isdigit():
            messagebox.showwarning("Atenção", "Páginas e Quantidade devem ser números inteiros.", parent=modal)
            return

        cursor.execute(
            "UPDATE livros SET titulo=?, autor=?, genero=?, paginas=?, quantidade=? WHERE id=?",
            (titulo, autor, genero, int(paginas), int(qtd), id_livro)
        )
        conexao.commit()
        messagebox.showinfo("Sucesso", "Livro atualizado!", parent=modal)
        atualizar_lista()
        modal.destroy()

    ctk.CTkButton(modal, text="Salvar Alterações", width=200, height=38,
                  font=("Segoe UI", 13, "bold"), command=salvar).grid(
        row=6, column=0, columnspan=2, pady=24)


# EXCLUIR LIVRO
def excluir_livro(master, id_livro, atualizar_lista):
    resposta = messagebox.askyesno("Confirmar", "Deseja excluir este livro?", parent=master)
    if resposta:
        cursor.execute("DELETE FROM livros WHERE id=?", (id_livro,))
        conexao.commit()
        atualizar_lista()


# MODAL: LISTAGEM DE USUÁRIOS (com Alterar/Excluir)
def abrir_listagem_usuarios(master):
    modal = ctk.CTkToplevel(master)
    modal.title("Usuários Cadastrados")
    modal.resizable(False, False)
    centralizar(modal, 880, 520)
    modal.grab_set()

    ctk.CTkLabel(modal, text="Usuários Cadastrados",
                 font=("Segoe UI", 18, "bold")).pack(pady=(20, 12))

    header = ctk.CTkFrame(modal, fg_color="#1a73e8", corner_radius=8)
    header.pack(padx=20, fill="x")

    colunas = ["Nome", "CPF", "Telefone", "E-mail", "Ações"]
    larguras = [200, 140, 140, 200, 160]
    for i, (col, larg) in enumerate(zip(colunas, larguras)):
        ctk.CTkLabel(header, text=col, width=larg,
                     font=("Segoe UI", 12, "bold"),
                     text_color="white").grid(row=0, column=i, padx=4, pady=8)

    scroll = ctk.CTkScrollableFrame(modal, height=340)
    scroll.pack(padx=20, pady=(4, 16), fill="both", expand=True)

    def carregar_dados():
        for widget in scroll.winfo_children():
            widget.destroy()

        cursor.execute("SELECT * FROM usuarios ORDER BY id DESC")
        registros = cursor.fetchall()

        if not registros:
            ctk.CTkLabel(scroll, text="Nenhum usuário cadastrado.",
                         font=("Segoe UI", 13), text_color="gray").pack(pady=30)
            return

        for idx, registro in enumerate(registros):
            id_usuario, nome, cpf, telefone, email = registro
            bg = "#f0f4ff" if idx % 2 == 0 else "#ffffff"
            linha = ctk.CTkFrame(scroll, fg_color=bg, corner_radius=6)
            linha.pack(fill="x", pady=2)

            valores = [nome, cpf, telefone, email]
            for i, (val, larg) in enumerate(zip(valores, larguras)):
                ctk.CTkLabel(linha, text=val, width=larg,
                             font=("Segoe UI", 12), anchor="center").grid(
                    row=0, column=i, padx=4, pady=8)

            acoes = ctk.CTkFrame(linha, fg_color="transparent")
            acoes.grid(row=0, column=4, padx=4, pady=4)

            ctk.CTkButton(acoes, text="Alterar", width=70, height=28,
                          font=("Segoe UI", 11),
                          command=lambda i=id_usuario: alterar_usuario(modal, i, carregar_dados)
                          ).grid(row=0, column=0, padx=3)

            ctk.CTkButton(acoes, text="Excluir", width=70, height=28,
                          font=("Segoe UI", 11), fg_color="#e74c3c", hover_color="#c0392b",
                          command=lambda i=id_usuario: excluir_usuario(modal, i, carregar_dados)
                          ).grid(row=0, column=1, padx=3)

    carregar_dados()


# MODAL: ALTERAR USUÁRIO
def alterar_usuario(master, id_usuario, atualizar_lista):
    cursor.execute("SELECT * FROM usuarios WHERE id=?", (id_usuario,))
    usuario = cursor.fetchone()
    if not usuario:
        return

    modal = ctk.CTkToplevel(master)
    modal.title("Alterar Usuário")
    modal.resizable(False, False)
    centralizar(modal, 560, 400)
    modal.grab_set()

    ctk.CTkLabel(modal, text="Alterar Usuário",
                 font=("Segoe UI", 18, "bold")).grid(
        row=0, column=0, columnspan=2, pady=(20, 10))

    e_nome     = campo(modal, "Nome", 1)
    e_nome.insert(0, usuario[1])
    e_cpf      = campo(modal, "CPF", 2)
    e_cpf.insert(0, usuario[2])
    e_telefone = campo(modal, "Telefone", 3)
    e_telefone.insert(0, usuario[3])
    e_email    = campo(modal, "E-mail", 4)
    e_email.insert(0, usuario[4])

    def salvar():
        nome     = e_nome.get().strip()
        cpf      = e_cpf.get().strip()
        telefone = e_telefone.get().strip()
        email    = e_email.get().strip()

        if not all([nome, cpf, telefone, email]):
            messagebox.showwarning("Atenção", "Preencha todos os campos.", parent=modal)
            return

        try:
            cursor.execute(
                "UPDATE usuarios SET nome=?, cpf=?, telefone=?, email=? WHERE id=?",
                (nome, cpf, telefone, email, id_usuario)
            )
            conexao.commit()
            messagebox.showinfo("Sucesso", "Usuário atualizado!", parent=modal)
            atualizar_lista()
            modal.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "CPF já cadastrado para outro usuário.", parent=modal)

    ctk.CTkButton(modal, text="Salvar Alterações", width=200, height=38,
                  font=("Segoe UI", 13, "bold"), command=salvar).grid(
        row=5, column=0, columnspan=2, pady=24)


# EXCLUIR USUÁRIO
def excluir_usuario(master, id_usuario, atualizar_lista):
    resposta = messagebox.askyesno("Confirmar", "Deseja excluir este usuário?", parent=master)
    if resposta:
        cursor.execute("DELETE FROM usuarios WHERE id=?", (id_usuario,))
        conexao.commit()
        atualizar_lista()


# JANELA PRINCIPAL 
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Biblioteca")
        self.resizable(False, False)
        centralizar(self, 540, 560)

        # Cabeçalho
        header = ctk.CTkFrame(self, fg_color="#1a73e8", corner_radius=0, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="📚  Sistema de Biblioteca",
                     font=("Segoe UI", 22, "bold"),
                     text_color="white").place(relx=0.5, rely=0.5, anchor="center")

        # Subtítulo
        ctk.CTkLabel(self, text="Controle de Empréstimo de Livros",
                     font=("Segoe UI", 13), text_color="gray").pack(pady=(18, 6))

        # Grade de botões
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(pady=20)

        botoes = [
            ("📖  Cadastrar Livro",      lambda: abrir_cadastro_livros(self)),
            ("👤  Cadastrar Usuário",    lambda: abrir_cadastro_usuarios(self)),
            ("🔄  Registrar Empréstimo", lambda: abrir_emprestimo(self)),
            ("📋  Livros Emprestados",   lambda: abrir_emprestados(self)),
            ("📑  Listar Livros",        lambda: abrir_listagem_livros(self)),
            ("🗂️  Listar Usuários",      lambda: abrir_listagem_usuarios(self)),
        ]

        for i, (texto, cmd) in enumerate(botoes):
            row, col = divmod(i, 2)
            ctk.CTkButton(
                frame, text=texto, width=220, height=70,
                font=("Segoe UI", 14, "bold"),
                corner_radius=12,
                command=cmd
            ).grid(row=row, column=col, padx=14, pady=14)

        # Rodapé
        ctk.CTkLabel(self, text="© 2025 Sistema de Biblioteca",
                     font=("Segoe UI", 10), text_color="#aaaaaa").pack(side="bottom", pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
    conexao.close()
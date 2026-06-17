# 📚 Library Management System — v2

A refined, function-based desktop application for managing a small library's catalog, members, and book loans, built with **Python**, **CustomTkinter**, and **SQLite**. This version improves on v1 with a styled header bar, centered modal windows, reusable form helpers, color-coded status badges, and stronger input validation.

## Overview

The app provides a simple graphical front-end over a local SQLite database, letting a librarian register books and users, hand out and track loans, and manage existing records — all without leaving the desktop.

## Features

- **Register Books** — title, author, genre, page count, and available quantity, with placeholder hints and numeric validation for pages/quantity.
- **Register Users** — full name, CPF (Brazilian ID), phone, and email, with duplicate-CPF detection.
- **Register Loans** — pick a user and an available book from dropdown lists; the due date is automatically set to **7 days** from the loan date, and the book's available quantity is decremented.
- **Loans Overview** — view *every* loan ever registered (not just active ones), each row showing a color-coded status badge (🟠 `Emprestado` / 🟢 `Devolvido`).
- **List Books** — browse the full catalog in a styled table, with inline **Edit** and **Delete** actions that refresh the list in place.
- **List Users** — browse every registered user in a styled table, with inline **Edit** and **Delete** actions that refresh the list in place.

## Tech Stack

| Component        | Technology                          |
|-------------------|--------------------------------------|
| Language           | Python 3                            |
| GUI Framework      | [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) |
| Database           | SQLite (via Python's built-in `sqlite3`) |
| Dialogs            | `tkinter.messagebox`                |
| Date handling      | `datetime`                          |

## Project Structure

```
.
├── Desafio_-_Sistema_de_Biblioteca_02.py   # Main application (single file)
└── biblioteca.db                            # SQLite database (created automatically on first run)
```

The app is organized as a set of standalone functions (`abrir_cadastro_livros`, `abrir_emprestimo`, `abrir_listagem_livros`, etc.) plus two small helpers:

- `centralizar(janela, largura, altura)` — centers any window on the screen.
- `campo(parent, label, row, placeholder)` — creates a labeled `CTkEntry` on a grid row, reused across every registration and edit form.

The `App` class (subclass of `ctk.CTk`) builds the main menu, with a blue header bar and a 3×2 grid of buttons that open each feature window.

## Database Schema

The database is created automatically the first time the app runs.

**`livros` (books)**

| Column      | Type    | Notes                |
|-------------|---------|-----------------------|
| id          | INTEGER | Primary key, autoincrement |
| titulo      | TEXT    | Required              |
| autor       | TEXT    | Required              |
| genero      | TEXT    | Required              |
| paginas     | INTEGER | Required, validated as integer |
| quantidade  | INTEGER | Required, validated as integer, available copies |

**`usuarios` (users)**

| Column    | Type | Notes                  |
|-----------|------|-------------------------|
| id        | INTEGER | Primary key, autoincrement |
| nome      | TEXT | Required                |
| cpf       | TEXT | Required, **unique** (duplicate insert/update is caught and reported to the user) |
| telefone  | TEXT | Required                |
| email     | TEXT | Required                |

**`emprestimos` (loans)**

| Column           | Type    | Notes                                    |
|-------------------|---------|--------------------------------------------|
| id                 | INTEGER | Primary key, autoincrement                 |
| usuario_id         | INTEGER | Foreign key → `usuarios.id`                |
| livro_id           | INTEGER | Foreign key → `livros.id`                  |
| data_emprestimo    | TEXT    | Loan date (`DD/MM/YYYY`)                   |
| data_devolucao     | TEXT    | Due date, 7 days after the loan date       |
| status             | TEXT    | `Emprestado` by default; shown as a colored badge in the loans list |

## Getting Started

### Prerequisites

- Python 3.9+
- `customtkinter`

### Installation

```bash
pip install customtkinter
```

### Running the app

```bash
python Desafio_-_Sistema_de_Biblioteca_02.py
```

On first launch, the script creates `biblioteca.db` in the same folder and sets up all required tables.

## What's Different from v1

- Modal windows are centered on screen via a shared `centralizar()` helper instead of a fixed `geometry()` string.
- Form fields are built with a single reusable `campo()` helper, reducing duplicated layout code.
- Tables use alternating row colors (zebra striping) and a colored header bar for readability.
- The loans list shows **all** loans with a status badge, instead of filtering to active ones only.
- Registration and edit forms validate that pages/quantity are integers and gracefully handle duplicate CPFs instead of crashing.

## Screenshots

> Add screenshots of the main menu and each window here, e.g.:
>
> ```markdown
> ![Main menu](screenshots/main-menu.png)
> ![Loans overview](screenshots/loans-overview.png)
> ```

## License

This project was built as a learning exercise. Feel free to add a license of your choice (e.g. MIT) before publishing if you'd like others to reuse the code.

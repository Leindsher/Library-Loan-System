# 📚 Library Management System — v1

A lightweight desktop application for managing a small library's catalog, members, and book loans. Built with **Python**, **CustomTkinter**, and **SQLite**, this version follows a single-class, object-oriented structure where the main window owns all sub-windows and database operations.

## Overview

The app provides a simple graphical front-end over a local SQLite database, letting a librarian register books and users, hand out and track loans, and manage existing records — all without leaving the desktop.

## Features

- **Register Books** — title, author, genre, page count, and available quantity.
- **Register Users** — full name, CPF (Brazilian ID), phone, and email.
- **Register Loans** — pick a user and an available book from dropdown lists; the due date is automatically set to **14 days** from the loan date, and the book's available quantity is decremented.
- **Active Loans** — view all loans currently marked as `Emprestado` (on loan).
- **List Books** — browse every book in the catalog, with inline **Edit** and **Delete** actions.
- **List Users** — browse every registered user, with inline **Edit** and **Delete** actions.

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
├── Desafio_-_Sistema_de_Biblioteca_01.py   # Main application (single file)
└── biblioteca.db                            # SQLite database (created automatically on first run)
```

All GUI logic lives in the `SistemaLivros` class, which builds the main menu and opens each feature in a `CTkToplevel` window.

## Database Schema

The database is created automatically the first time the app runs.

**`livros` (books)**

| Column      | Type    | Notes                |
|-------------|---------|-----------------------|
| id          | INTEGER | Primary key, autoincrement |
| titulo      | TEXT    | Required              |
| autor       | TEXT    | Required              |
| genero      | TEXT    | Required              |
| paginas     | INTEGER | Required              |
| quantidade  | INTEGER | Required, available copies |

**`usuarios` (users)**

| Column    | Type | Notes                  |
|-----------|------|-------------------------|
| id        | INTEGER | Primary key, autoincrement |
| nome      | TEXT | Required                |
| cpf       | TEXT | Required, **unique**    |
| telefone  | TEXT | Required                |
| email     | TEXT | Required                |

**`emprestimos` (loans)**

| Column           | Type    | Notes                                    |
|-------------------|---------|--------------------------------------------|
| id                 | INTEGER | Primary key, autoincrement                 |
| usuario_id         | INTEGER | Foreign key → `usuarios.id`                |
| livro_id           | INTEGER | Foreign key → `livros.id`                  |
| data_emprestimo    | TEXT    | Loan date (`YYYY-MM-DD`)                   |
| data_devolucao     | TEXT    | Due date, 14 days after the loan date      |
| status             | TEXT    | Defaults to `Emprestado` (on loan)         |

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
python Desafio_-_Sistema_de_Biblioteca_01.py
```

On first launch, the script creates `biblioteca.db` in the same folder and sets up all required tables.

## Known Limitations

- CPF uniqueness is enforced at the database level, but the registration form does not currently catch the resulting error — registering a duplicate CPF will raise an unhandled exception instead of showing a friendly message.
- Numeric fields (pages, quantity) are not validated before being saved; non-numeric input can cause errors.
- The interface uses CustomTkinter's light appearance mode by default.

## Screenshots

> Add screenshots of the main menu and each window here, e.g.:
>
> ```markdown
> ![Main menu](screenshots/main-menu.png)
> ![Book registration](screenshots/register-book.png)
> ```

## License

This project was built as a learning exercise. Feel free to add a license of your choice (e.g. MIT) before publishing if you'd like others to reuse the code.

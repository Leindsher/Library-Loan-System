# 📚 Library Management System

A desktop application for managing a small library's catalog, members, and book loans, built with **Python**, **CustomTkinter**, and **SQLite**.

This repository contains **two implementations of the same project**, written as part of a learning challenge to practice GUI development and database integration with Python. Both versions share the same core idea — register books, register users, manage loans — but differ in code structure and a few UX details, as explained below.

## Repository Structure

```
.
├── Desafio_-_Library-Loan-System 01.py   # Version 1 — class-based UI
├── Desafio_-_Library-Loan-System 02.py   # Version 2 — function-based UI with modals
└── biblioteca.db                            # SQLite database (created automatically on first run)
```

> Both scripts use the same database file name and schema, so only run one version at a time against a given `biblioteca.db` — or point each version to its own copy of the file.

## Features

Both versions provide the same core functionality:

- **Register Books** — title, author, genre, page count, and available quantity.
- **Register Users** — full name, CPF (Brazilian ID), phone, and email.
- **Register Loans** — pick a user and an available book from dropdown lists; the due date is calculated automatically and the book's available quantity is decremented.
- **Loans Overview** — view registered loans.
- **List Books** — browse the catalog with inline **Edit** and **Delete** actions.
- **List Users** — browse registered users with inline **Edit** and **Delete** actions.

## Version Comparison

| Aspect                  | v1 (`...01.py`)                              | v2 (`...02.py`)                                            |
|--------------------------|-----------------------------------------------|--------------------------------------------------------------|
| Architecture              | Single `SistemaLivros` class; windows are methods | Standalone functions plus an `App(ctk.CTk)` main window     |
| Form fields                | Built inline for each window                | Reusable `campo()` helper generates a labeled entry on a grid row |
| Window positioning         | Fixed `geometry()` string                   | Centered on screen via a shared `centralizar()` helper       |
| Loan due date               | 14 days after the loan date                 | 7 days after the loan date                                   |
| Loan date format             | `YYYY-MM-DD`                                | `DD/MM/YYYY`                                                  |
| Loans Overview                | Shows only active (`Emprestado`) loans     | Shows **all** loans, with a color-coded status badge (🟠 on loan / 🟢 returned) |
| Table styling                  | Plain rows                                  | Alternating row colors (zebra striping) + colored header bar |
| Numeric field validation         | None — non-numeric input can cause errors | Pages/quantity are validated as integers before saving       |
| Duplicate CPF handling             | Not handled (raises an unhandled exception) | Caught with `try/except sqlite3.IntegrityError` and reported to the user |
| Appearance mode                      | Light                                       | Light                                                          |

## Tech Stack

| Component        | Technology                          |
|-------------------|--------------------------------------|
| Language           | Python 3                            |
| GUI Framework      | [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) |
| Database           | SQLite (via Python's built-in `sqlite3`) |
| Dialogs            | `tkinter.messagebox`                |
| Date handling      | `datetime`                          |

## Database Schema

The database is created automatically the first time either script runs.

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
| data_emprestimo    | TEXT    | Loan date (format differs by version — see comparison table) |
| data_devolucao     | TEXT    | Due date (14 days in v1, 7 days in v2)     |
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
# Version 1
python Desafio_-_Sistema_de_Biblioteca_01.py

# Version 2
python Desafio_-_Sistema_de_Biblioteca_02.py
```

On first launch, the script creates `biblioteca.db` in the same folder and sets up all required tables.


## License

This project was built as a learning exercise.

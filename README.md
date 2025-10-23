# Banking System

This Python project provides a simple command-line banking application with a persistent SQLite backend. It supports creating new accounts, secure login, checking balances, adding income, and performing validated transfers using the Luhn algorithm. The system cleanly separates database access from business logic for clarity and maintainability.

## Features

* **Account Management:** Create accounts with automatically generated card numbers and 4-digit PINs.
* **Persistent Storage:** Uses SQLite for durable data storage—no external dependencies.
* **Luhn Validation:** Ensures valid account numbers using the Luhn checksum algorithm.
* **Balance Operations:** Deposit income, check balance, and transfer funds securely.
* **CLI Interface:** Simple text-based menus for interaction.
* **Modular Architecture:** `BankDatabase` handles SQL; `BankApp` manages user flow.

## How to Use

**Run the app:**

```bash
python banking.py
```

A new database (`card.s3db`) will be created automatically. Follow on-screen prompts to create accounts and perform transactions.

## Code Overview

* `bank_database.py` – Handles SQLite connections and CRUD operations (insert, update, delete, transfer).
* `bank_app.py` – Manages user menus, account logic, and validation.
* `banking.py` – Entry point; launches the interactive console loop.

## Roadmap

* Add password hashing for PINs.
* Integrate transaction history logging.

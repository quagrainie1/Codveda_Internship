# Codveda Internship

Python programming tasks completed as part of the Codveda internship program.
Two tasks per level, organised into separate folders.

---

## Repository Structure

```
Codveda_Internship/
├── Level1/
│   ├── task1_calculator.py        — Simple Calculator
│   └── task2_guessing_game.py     — Number Guessing Game
├── Level2/
│   ├── task1_todo_list.py         — To-Do List Application
│   └── task2_word_counter.py      — Data Scrapper
└── Level3/
    ├── task1_encryption.py        — File Encryption / Decryption
    └── task2_nqueens.py           — N-Queens Problem Solver
```

---

## Level 1 — Basic

### Task 1 · Simple Calculator
Performs addition, subtraction, multiplication, and division.
Handles division by zero with a clear error message.
```bash
python Level1/task1_calculator.py
```
**Key concepts:** functions, user input, error handling, while loop menu

### Task 2 · Number Guessing Game
Generates a random number (1–100). Gives "Too high / Too low / Very close"
hints over 10 attempts. Tracks wins and losses across rounds.
```bash
python Level1/task2_guessing_game.py
```
**Key concepts:** `random` module, loops, conditionals, score tracking

---

## Level 2 — Intermediate

### Task 1 · To-Do List Application
Command-line task manager stored in `tasks.json`.
Add, view, mark done, delete, and clear completed tasks.
```bash
python Level2/task1_todo_list.py
```
**Key concepts:** JSON file I/O, CRUD operations, dictionaries, error handling

### Task 2 · Data Scraper
Scrapes news headlines from BBC News, Hacker News, and Reuters. 
Displays results in the terminal and optionally saves them to a timestamped CSV file.
```bash
python Level2/task2_data_scraper.py
```
**Key concepts: web scraping, requests, BeautifulSoup, HTML parsing, CSV writing, exception handling

## Level 3 — Advanced

### Task 1 · File Encryption / Decryption
Encrypts and decrypts files using Caesar Cipher or Fernet (AES).
```bash
pip install cryptography    # for Fernet mode only
python Level3/task1_encryption.py
```
**Key concepts:** file I/O, modular arithmetic, `cryptography` library, argparse

### Task 2 · N-Queens Problem
Places N queens on an N×N board so none attack each other.
Prints visual ♛ chessboard solutions and solving statistics.
```bash
python Level3/task2_nqueens.py
```
**Key concepts:** backtracking, recursion, constraint tracking with sets

---

## Install dependencies
```bash
pip install cryptography   # only needed for Fernet encryption (Level 3 Task 1)
```

---
*Codveda Internship — Python Development Track*

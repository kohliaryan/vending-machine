# 🥤 Smart Vending Machine API

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109%2B-009688?style=for-the-badge&logo=fastapi)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0_(Async)-red?style=for-the-badge&logo=sqlalchemy)
![uv](https://img.shields.io/badge/Built_with-uv-purple?style=for-the-badge)

A high-performance, asynchronous REST API designed to manage a digital vending machine's inventory and transactions. Built with modern Python practices, including **FastAPI**, **SQLAlchemy 2.0 (Async)**, and **Pydantic V2**.

---

## 🚀 Features

- **Asynchronous Architecture:** Fully non-blocking database operations using `aiosqlite`.
- **Inventory Management:** Add, update, and monitor stock levels.
- **Transaction Logic:** Handles purchases, calculates change, and validates stock availability atomically.
- **Robust Validation:** Automatic request validation using Pydantic models.
- **Modern Tooling:** Dependency management and execution handled by `uv`.

---

## 🛠️ Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Database:** SQLite (with `aiosqlite` driver)
- **ORM:** SQLAlchemy 2.0 (Async)
- **Validation:** Pydantic
- **Package Manager:** [uv](https://github.com/astral-sh/uv)

---

## ⚡ Getting Started

This project uses **uv** for lightning-fast dependency management.

### 1. Prerequisites
Ensure you have `uv` installed.
```bash
# On macOS/Linux
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh

# On Windows
powershell -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"
```
### 2. Clone the Repository
```bash
git clone https://github.com/kohliaryan/vending-machine.git
cd fastapi-vending-machine
```
### 3. Install Dependencies
Instead of creating a virtual environment manually, let uv handle it:
```bash
uv sync
```
### 4. Configure Environment Variables
Create a .env file in the root directory to keep your configuration safe.
```bash
touch .env
```
### 5. Run the Server
Use uv run to execute the application within the managed environment:

```Bash
uv run uvicorn main:app --reload
The server will start at http://127.0.0.1:8000.
```
## 📚 API Documentation

Once the server is running, you can access the interactive documentation:

* **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Key Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/items` | List all items. Supports filtering by price via `?max_price=VALUE`. |
| `POST` | `/items` | **(Admin)** Add a new item to the global inventory. |
| `GET` | `/items/{item_id}` | Retrieve details for a specific item by ID. |
| `POST` | `/items/{item_id}/buy` | Purchase an item. Handles stock reduction and change calculation. |
| `PUT` | `/items/{item_id}` | **(Admin)** Update the stock quantity for an existing item. |

## 📂 Project Structure

The project follows a modular architecture to separate concerns between database logic, API routes, and data validation.

```text
.
├── main.py            # Application entry point; initializes FastAPI and includes routers
├── database.py        # Async Database setup, engine creation, and dependency injection
├── models.py          # SQLAlchemy 2.0 DB Models (Table definitions)
├── schemas.py         # Pydantic Schemas for Request/Response validation
├── routes.py          # API Endpoints and business logic
├── .env               # Environment variables (Database URL, Secrets) - GitIgnored
├── .gitignore         # Specifies files to exclude from Git (e.g., .env, *.db)
├── pyproject.toml     # Project metadata and dependencies (managed by uv)
└── uv.lock            # Lockfile ensuring reproducible dependency versions
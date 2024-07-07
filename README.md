# Auth Service with FastAPI and JWT Authentication

## Summary

This project implements an authentication service using FastAPI with JWT authentication. The service provides endpoints for user registration, login, and token verification. It uses SQLAlchemy for database interactions and Passlib for password hashing.

## Project Structure
```
auth_service/
│
├── main.py
├── models.py
├── routes.py
├── auth.py
├── database.py
├── schemas.py
├── requirements.txt
└── tests/
    ├── init.py
    └── test_auth.py
````

## Requirements

- Python 3.6+
- FastAPI
- Uvicorn
- SQLAlchemy
- Passlib
- Pydantic
- Python-JOSE
- Pytest
- Httpx

## Installation

1. **Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

    pip install -r requirements.txt

## How to run server 
``
python main.py
``

The API should now be running and accessible at http://127.0.0.1:8000.

## How to run tests
``
    pytest
``


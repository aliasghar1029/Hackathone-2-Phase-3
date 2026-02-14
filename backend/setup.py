from setuptools import setup, find_packages

setup(
    name="todo-backend",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "sqlmodel",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "python-multipart",
        "google-generativeai",
        "python-dotenv",
        "SQLAlchemy-Utils",
    ],
)

from flask_sqlalchemy import SQLAlchemy
# Создаем экземпляры здесь
db = SQLAlchemy()

from .user import User
from .Book import Book
__all__ = ['db', 'User', "Book"]
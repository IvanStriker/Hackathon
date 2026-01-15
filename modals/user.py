from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .base import BaseModel
from . import db


class User(BaseModel, UserMixin):
    """Модель пользователя"""
    __tablename__ = 'users'

    # Основные поля
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    avatar = db.Column(db.String(200), default='default_avatar.png')
    bio = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)

    # Связи
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')
    ratings = db.relationship('Rating', backref='user', lazy=True, cascade='all, delete-orphan')
    reading_lists = db.relationship('ReadingList', backref='user', lazy=True, cascade='all, delete-orphan')

    # Связь многие-ко-многим для избранных книг
    favorite_books = db.relationship('Book',
                                     secondary='user_favorites',
                                     lazy='subquery',
                                     backref=db.backref('favorited_by', lazy=True))

    def set_password(self, password):
        """Хеширование пароля"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Проверка пароля"""
        return check_password_hash(self.password_hash, password)

    def get_full_name(self):
        """Полное имя пользователя"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    def is_favorite(self, book):
        """Проверить, находится ли книга в избранном"""
        return book in self.favorite_books

    def to_dict(self):
        """Преобразование пользователя в словарь"""
        data = super().to_dict()
        data.update({
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.get_full_name(),
            'avatar': self.avatar,
            'bio': self.bio,
            'is_admin': self.is_admin,
            'last_login': self.last_login.isoformat() if self.last_login else None
        })
        return data

    def __repr__(self):
        return f'<User {self.username}>'
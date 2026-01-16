from datetime import datetime
from sqlalchemy import func
from .base import BaseModel
from . import db

class Book(BaseModel):
    """Модель книги"""
    __tablename__ = 'books'

    # Основные поля
    title = db.Column(db.String(200), nullable=False, index=True)
    author = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text)
    isbn = db.Column(db.String(13), unique=True)  # ISBN-13
    publication_year = db.Column(db.Integer)
    cover_image = db.Column(db.String(300), default='default_cover.jpg')
    pages = db.Column(db.Integer)
    publisher = db.Column(db.String(200))
    language = db.Column(db.String(50), default='Русский')

    # Связи
    reviews = db.relationship('Review', backref='book', lazy=True, cascade='all, delete-orphan')
    ratings = db.relationship('Rating', backref='book', lazy=True, cascade='all, delete-orphan')

    # Связь многие-ко-многим с жанрами
    genres = db.relationship('Genre',
                             secondary='book_genres',
                             lazy='subquery',
                             backref=db.backref('books', lazy=True))


    @property
    def ratings_count(self):
        """Количество оценок"""
        return len(self.ratings)

    @property
    def reviews_count(self):
        """Количество отзывов"""
        return len(self.reviews)

    def add_genre(self, genre):
        """Добавить жанр книге"""
        if genre not in self.genres:
            self.genres.append(genre)
            self.save()
            return True
        return False

    def remove_genre(self, genre):
        """Удалить жанр у книги"""
        if genre in self.genres:
            self.genres.remove(genre)
            self.save()
            return True
        return False


    def to_dict(self):
        """Преобразование книги в словарь"""
        data = super().to_dict()
        data.update({
            'title': self.title,
            'author': self.author,
            'description': self.description,
            'isbn': self.isbn,
            'publication_year': self.publication_year,
            'cover_image': self.cover_image,
            'pages': self.pages,
            'publisher': self.publisher,
            'language': self.language,
            'average_rating': self.average_rating,
            'ratings_count': self.ratings_count,
            'reviews_count': self.reviews_count,
            'genres': [genre.name for genre in self.genres]
        })
        return data

    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'
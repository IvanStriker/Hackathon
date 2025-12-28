from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Integer, String, ForeignKey
from db.base import db
import re

# Prevent circular import
if TYPE_CHECKING:
    from .bookarchive import BookArchive
    from .book import Book

class User(db.Model):
    """Create a model class"""
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(db.String(120), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(db.String(120), unique=True, nullable=True)
    # archive_id: Mapped[Optional[int]] = mapped_column(ForeignKey("bookarchive.id"),unique=True, nullable=True)
    
    # Relationship to BookArchive (each user has only one book archive)
    # book_archive: Mapped["BookArchive"] = relationship("BookArchive", back_populates="user")
    book_archive: Mapped["BookArchive"] = relationship(
        "BookArchive", 
        back_populates="user", 
        uselist=False,  # each user has only one book archive
        lazy="joined"
    )

    @validates('name')
    def validate_name(self, key, name):
        if len(name) > 120 or not (isinstance(name, str)) or re.match(r"\d", name):
            raise ValueError("Invalid user name")
        return name
    
    @validates('email')
    def validate_email(self, key, address):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", address):
            raise ValueError("Invalid email address")
        return address
    
    # добавлять книги в каталог,
    # редактировать сведения,
    # удалять записи,
    # отмечать статус чтения,
    # просматривать каталог.

    def add_to_archive(self, book):
        from models.bookarchive import BookArchive
        from models.book import Book

        if not self.book_archive:
            self.book_archive = BookArchive(user_id=self.id)
            db.session.add(self.book_archive)
            db.session.flush()  # Take ID for book_archive

        book.archive_id = self.book_archive.id

        db.session.add(book)
        db.session.commit()

        return book

    # def modify_infor():
    #     db.session.add(Book)
    #     db.session.commit()

    # def remove_from_archive():
    #     db.session.add(Book)
    #     db.session.commit()

    # def mark_reading_status():
    #     db.session.add(Book)
    #     db.session.commit()

    # def view_archive():
    #     db.session.add(Book)
    #     db.session.commit()


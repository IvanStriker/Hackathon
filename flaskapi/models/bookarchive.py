from typing import List, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from db.base import db

# Prevent circular import
if TYPE_CHECKING:
    from .book import Book
    from .user import User

class BookArchive(db.Model):
    __tablename__ = "bookarchive"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    
    # # Backref to User (one-to-one)
    # user: Mapped["User"] = relationship("User", back_populates="book_archive")
    
    # # relationship to Book (one-to-many)
    # books: Mapped[List["Book"]] = relationship("Book", back_populates="book_archive")

    # Add user_id to create foreign key to User
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), 
        unique=True,  # ensure that each user has only one BookArchive
        nullable=False
    )
    
    # Relationship to User
    user: Mapped["User"] = relationship("User", back_populates="book_archive")
    
    # Relationship to Book
    books: Mapped[List["Book"]] = relationship("Book", back_populates="archive")
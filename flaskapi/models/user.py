from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy import Integer, String, JSON
from db.base import db
import re

class User(db.Model):
    """Create a model class"""
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(db.String(120), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(db.String(120), unique=True, nullable=True)
    # archive: Mapped[list] = mapped_column(db.JSON, default=list, unique=False, nullable=True)

    @validates('name')
    def validate_name(self, key, name):
        if len(name) > 120 or not (isinstance(name, str)) or re.match(r"\d", name):
            raise ValueError("Invalid user name")
        return name
    
    @validates('email')
    def validate_email(self, key, address):
        if '@' not in address:
            raise ValueError("Invalid email address")
        return address
    
    # добавлять книги в каталог,
    # редактировать сведения,
    # удалять записи,
    # отмечать статус чтения,
    # просматривать каталог.

    # def add_to_archive():
    #     db.session.add(Book)
    #     db.session.commit()

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


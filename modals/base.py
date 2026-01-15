from . import db
from datetime import datetime

class BaseModel(db.Model):
    """Абстрактный базовый класс для всех моделей"""
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Сохранение объекта в БД"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Удаление объекта из БД"""
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        """Обновление полей объекта"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()

    @classmethod
    def get_all(cls):
        """Получение всех записей"""
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        """Получение записи по ID"""
        return cls.query.get(id)

    @classmethod
    def filter_by(cls, **kwargs):
        """Фильтрация записей"""
        return cls.query.filter_by(**kwargs)

    def to_dict(self):
        """Преобразование объекта в словарь (для API)"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
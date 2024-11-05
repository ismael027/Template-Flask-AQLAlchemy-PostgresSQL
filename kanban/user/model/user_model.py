from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    password: Mapped[str]
    email: Mapped[str]
    photo: Mapped[Optional[str]]
    created_at: Mapped[Optional[datetime]] = mapped_column(
        default=datetime.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        default=datetime.now()
    )

    cards: Mapped[List['Card']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )
    
    categories: Mapped[List['Category']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )
 
    @property
    def is_authenticated(self):
        return False

    @property
    def is_active(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return str(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'password': self.password,
            'email': self.email,
            'photo': self.photo,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'cards': [card.to_dict() for card in self.cards],
        }


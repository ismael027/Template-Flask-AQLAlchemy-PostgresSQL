from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, Table, Column, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

class Base(DeclarativeBase):
    pass

card_category_table = Table(
    'card_category',
    Base.metadata,
    Column('card_id', String, ForeignKey('cards.id')),
    Column('category_id', String, ForeignKey('categories.id')),
)

class Card(Base):
    __tablename__ = 'cards'
    id: Mapped[str] = mapped_column(primary_key=True)
    status: Mapped[str]
    title: Mapped[str]
    description: Mapped[Optional[str]]
    created_at: Mapped[Optional[datetime]] = mapped_column(
        default=datetime.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        default=datetime.now()
    )

    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='cards')
    
    categories: Mapped[List['Category']] = relationship(
        secondary=card_category_table, back_populates='cards')

    def to_dict(self):
        return {
            'id': self.id,
            'status': self.status,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'user_id': self.user_id,
            'categories': [category.id for category in self.categories],
        }
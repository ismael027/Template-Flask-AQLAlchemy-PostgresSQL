from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

from kanban.card.model.card_model import card_category_table

class Base(DeclarativeBase):
    pass

class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    color: Mapped[str]
    created_at: Mapped[Optional[datetime]] = mapped_column(
        default=datetime.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        default=datetime.now()
    )
    
    cards: Mapped[List['Card']] = relationship(
        secondary=card_category_table, back_populates='categories'
    )

    user_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE')
    )
    user: Mapped['User'] = relationship(back_populates='categories')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'cards': [card.id for card in self.cards],
        }
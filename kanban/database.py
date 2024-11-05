from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from kanban.config import get_config
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = create_engine(get_config()['DATABASE_URI'])
Session = sessionmaker(db)
Base.metadata.create_all(db)

def init_db():
    Base.metadata.create_all(db)

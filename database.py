from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# sqlite engine instance
engine = create_engine("sqlite:///phonebook.db")

# DeclarativeMeta instance
Base = declarative_base()

# session local class
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

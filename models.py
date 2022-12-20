from sqlalchemy import create_engine, Column, String, Integer
from database import Base

class PhoneBook(Base):
    __tablename__ = 'phonebook'
    name = Column(String(256))
    phoneNumber = Column(String(256), primary_key=True, unique=True)
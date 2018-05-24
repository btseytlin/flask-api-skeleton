from sqlalchemy import Column, Integer, String
from .base import Base


class Kitty(Base):
    __tablename__ = 'kitties'
    id = Column(Integer, primary_key=True)
    name = Column(String)
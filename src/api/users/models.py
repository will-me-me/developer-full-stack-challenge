from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import column_property
from sqlalchemy.sql import select, func
from sqlalchemy.ext.hybrid import hybrid_property

from db import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    

class Author(Base):
    __tablename__ = "authors"
        
    id = Column(Integer, primary_key=True, index=True )
    name = Column(String, unique=True, index=True)
    books = relationship("Books", back_populates="author")
    
    @hybrid_property
    def total_books(self):
        return len(self.books)
    
    class Config:
        orm_mode = True

class Books(Base):
    __tablename__ = "books"
        
    id = Column(Integer, primary_key=True, index=True , autoincrement=True, unique=True)
    name = Column(String, unique=True, index=True)
    page_numbers = Column(Integer)
    author_id = Column(Integer, ForeignKey("authors.id"))
    # author_name = column_property(select([Author.name]).where(Author.id == author_id))

    author = relationship("Author", back_populates="books")

    class Config:
        orm_mode = True


        
        

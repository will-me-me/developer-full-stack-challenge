from pydantic import BaseModel, Field
from typing import Optional, List

# from . models import User, Author, Books

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    hashed_password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class LoginUser(BaseModel):
    username: str
    password: str

class AuthorBase(BaseModel):
    name: str

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    total_books: Optional[int] = 0

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    name: str
    page_numbers: int
    author_name: Optional[str] = None
    author_id: Optional[int] = None

class BookCreate(BookBase):
    pass

class Books(BookBase):
    id: int
    author: Optional[Author] = None

    class Config:
        orm_mode = True

class UpdateBook(BaseModel):
    name: Optional[str] = None
    page_numbers: Optional[int] = None
    author_name: Optional[str] = None
    author_id: Optional[int] = None

class AddbookToAuthor(BaseModel):
    name: str
    page_numbers: int
    

Author.update_forward_refs()
Books.update_forward_refs()






    



    
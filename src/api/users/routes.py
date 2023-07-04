from typing import List, Optional
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi import FastAPI, Depends, status, Response, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db import SessionLocal, engine

# from helpers import create_user, user_login, create_author,update_author, create_book, update_book
import users.helpers as helpers
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime

import users.models as models
import users.schemas as schemas

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create_user", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = helpers.get_user_by_email(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return helpers.create_user(db, user)


@router.post("/login")
def login(user: schemas.LoginUser, db: Session = Depends(get_db)):
    return helpers.user_login(db, user)


@router.post("/create_author", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return helpers.create_author(db, author)


@router.post("/create_book", response_model=schemas.Books)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return helpers.create_book(db, book)


@router.get("/get_all_authors", response_model=List[schemas.Author])
def get_all_authors(db: Session = Depends(get_db)):
    return helpers.get_all_authors(db)


@router.get("/get_all_books", response_model=List[schemas.Books])
def get_all_books(db: Session = Depends(get_db)):
    return helpers.get_all_books(db) 

@router.delete("/delete_book/{id}")
def delete_book(id: int, db: Session = Depends(get_db)):
    return helpers.delete_book_by_id(db, id)

@router.delete("/delete_author/{id}")
def delete_author(id: int, db: Session = Depends(get_db)):
    return helpers.delete_author_by_id(db, id)

@router.put("/update_book/{id}")
def update_book(id: int, book: schemas.UpdateBook, db: Session = Depends(get_db)):
    return helpers.update_book(db, id, book)

@router.get("/get_author_books/{id}", response_model=List[schemas.Books])
def get_author_books(id: int, db: Session = Depends(get_db)):
    return helpers.get_books_given_author(db, id)

@router.post("/addbook_to_author/{author_id}", response_model=schemas.Books)
def addbook_to_author(author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    return helpers.addbook_by_author(db, author_id, book)



















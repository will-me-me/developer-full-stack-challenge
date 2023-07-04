import bcrypt
from fastapi import HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from auth.jwt_handler import sign_jwt
from . import models, schemas

class TokenResponse(BaseModel):
    token: str
    token_type: str
    user : schemas.User


def encrypt_password(password: str):
    print("password:", password)
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

def check_encrypted_password(password: str, hashed_password: str):
    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode()
    )

def get_user_by_email(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = encrypt_password(user.hashed_password)
    db_user = models.User(
        username = user.username,
        hashed_password = hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def user_login(db: Session, user: schemas.LoginUser):
    username = user.username
    password = user.password
    db_user = get_user_by_email(db, username)
    if not db_user:
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    if not check_encrypted_password(password, db_user.hashed_password):
        raise HTTPException(status_code=404, detail="Incorrect password")
    
    user_data = {
        "username": db_user.username,
        "id": db_user.id
    }
    user_data = {**user_data}
    access_token = sign_jwt(user_data)
    return TokenResponse(token=access_token, token_type="bearer", user=db_user)

def create_author(db: Session, author: schemas.AuthorCreate):
    '''check if author exists'''
    db_author = db.query(models.Author ).filter(models.Author.name == author.name).first()
    if db_author:
        raise HTTPException(status_code=400, detail="Author already exists")
    '''create author'''
    db_author = models.Author(
        name = author.name
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    print("added ")
    return db_author

def get_all_authors(db: Session):
    '''get all authors'''
    users = db.query(models.Author).offset(0).limit(100).all()
    return users

def get_author_id(db: Session, author_name: str):
    '''return the id of the author'''
    author = db.query(models.Author).filter(models.Author.name == author_name).first()
    if author:
        author_id = author.id
        return author_id
    else:
        return None



def create_book(db: Session, book: schemas.BookCreate):
    '''check if book exists'''
    db_book = db.query(models.Books).filter(models.Books.name == book.name).first()
    if db_book:
        raise HTTPException(status_code=400, detail="Book already exists")
    '''check if author exists'''
    db_author = db.query(models.Author).filter(models.Author.id == book.author_name).first()
    print("db_author:", db_author)
    author_id = get_author_id(db, book.author_name)
    print("author_id:", author_id)
    if not author_id:
        raise HTTPException(status_code=400, detail="Author does not exist")
    '''create book'''
    db_book = models.Books(
        name = book.name,
        page_numbers = book.page_numbers,
        # author_name = book.author_name,
        author_id = author_id
    )
    print("db_book:", db_book.author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_all_books(db: Session):
    '''get all books'''
    return db.query(models.Books).all()


def delete_author_by_id(db: Session, author_id: int):
    '''check if author exists'''
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=400, detail="Author does not exist")
    '''delete author'''
    db.query(models.Author).filter(models.Author.id == author_id).delete()
    db.commit()
    return {"message": "author with id: {} deleted successfully".format(author_id)}

def delete_book_by_id(db: Session, book_id: int):
    '''check if book exists'''
    db_book = db.query(models.Books).filter(models.Books.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=400, detail="Book does not exist")
    '''delete book'''
    db.query(models.Books).filter(models.Books.id == book_id).delete()
    db.commit()
    return {"message": "book with id: {} deleted successfully".format(book_id)}

def update_book(db: Session, book_id: int, book: schemas.UpdateBook):
    '''check if book exists'''
    db_book = db.query(models.Books).filter(models.Books.id == book_id).first()
    print("db_book:", db_book)
    if not db_book:
        raise HTTPException(status_code=400, detail="Book does not exist")
    '''check if author exists'''
    db_author = db.query(models.Author).filter(models.Author.id == book.author_name).first()
    print("db_author:", db_author)
    author_id = get_author_id(db, book.author_name)
    print("author_id:", author_id)
    if not author_id:
        raise HTTPException(status_code=400, detail="Author does not exist")
    '''update book'''
    db.query(models.Books).filter(models.Books.id == book_id).update({
        "name": book.name,
        "page_numbers": book.page_numbers,
        "author_id": author_id
    })
    db.commit()
    return {"message": "book with id: {} updated successfully".format(book_id)}


def get_books_given_author(db: Session, author_id: int):
    '''check if author exists'''
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=400, detail="Author does not exist")
    '''get books given author'''
    books = db.query(models.Books).filter(models.Books.author_id == author_id).all()
    return books

def addbook_by_author(db: Session, author_id: int, book: schemas.BookCreate):
    '''check if author exists'''
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=400, detail="Author does not exist")
    '''check if book exists'''
    db_book = db.query(models.Books).filter(models.Books.name == book.name).first()
    if db_book:
        raise HTTPException(status_code=400, detail="Book already exists")
    '''create book'''
    db_book = models.Books(
        name = book.name,
        page_numbers = book.page_numbers,
        author_id = author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def Updated_book_by_book_id(db: Session, book_id: int, book: schemas.UpdateBook):
    '''check if book exists'''
    db_book = db.query(models.Books).filter(models.Books.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=400, detail="Book does not exist")
    '''check if author exists'''
    db_author = db.query(models.Author).filter(models.Author.id == book.author_name).first()
    print("db_author:", db_author)
    author_id = get_author_id(db, book.author_name)
    print("author_id:", author_id)
    if not author_id:
        raise HTTPException(status_code=400, detail="Author does not exist")
    '''update book'''
    db.query(models.Books).filter(models.Books.id == book_id).update({
        "name": book.name,
        "page_numbers": book.page_numbers,
        "author_id": author_id
    })
    db.commit()
    return {"message": "book with id: {} updated successfully".format(book_id)}

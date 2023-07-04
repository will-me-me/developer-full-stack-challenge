# postgress data base connection
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import psycopg2




engine = create_engine('sqlite:///database.db', echo=True, connect_args={"check_same_thread": False}, poolclass=StaticPool)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# from sqlalchemy import create_engine





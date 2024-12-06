from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/eprompt"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
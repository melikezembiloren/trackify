from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import Config

# Engine oluşturma
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

# Session factory oluşturma
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class oluşturma
Base = declarative_base()

# Session yönetimi için generator
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database bağlantısı için class
class DatabaseConnection:
    @staticmethod
    def get_db():
        return get_db()
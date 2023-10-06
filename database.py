from sqlalchemy import create_engine, Column, DateTime, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/coil_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class CoilDB(Base):
    __tablename__ = "coils"
    id = Column(Integer, primary_key=True, index=True)
    length = Column(Float)
    weight = Column(Float)
    created_at = Column(DateTime)
    deleted_at = Column(DateTime, nullable=True)

Base.metadata.create_all(bind=engine)
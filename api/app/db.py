import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

database_url = os.getenv("DATABASE_URL")
if not database_url:
    user = os.getenv("POSTGRES_USER", "radar")
    password = os.getenv("POSTGRES_PASSWORD", "radar_dev_password")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "cluster_radar")
    database_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"

engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
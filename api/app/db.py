import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# defaults match docker-compose values, override via env var in k8s later
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://radar:radar_dev_password@localhost:5432/cluster_radar")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
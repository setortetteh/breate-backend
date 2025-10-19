import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# ------------------------------------------
# Load environment variables from .env
# ------------------------------------------
# Works whether you run from root or inside breate_backend/
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# ------------------------------------------
# Get DATABASE_URL from environment
# ------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is missing! Please check your .env file in the project root.")

# ------------------------------------------
# Database setup
# ------------------------------------------
# Neon requires SSL
engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"},
    echo=False  # set to True if you want to see SQL logs
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ------------------------------------------
# Dependency for DB session
# ------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

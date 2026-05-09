from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./db/aura-score.db"

# connection object to the database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# session for staging changes
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/telegram_warehouse"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
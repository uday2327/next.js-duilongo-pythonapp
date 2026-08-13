import os
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./duolingo_clone.db")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from app import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    ensure_sqlite_columns()


def ensure_sqlite_columns():
    if not DATABASE_URL.startswith("sqlite"):
        return
    inspector = inspect(engine)
    if "courses" not in inspector.get_table_names():
        return
    columns = {column["name"] for column in inspector.get_columns("courses")}
    with engine.begin() as connection:
        if "source_language_id" not in columns:
            connection.execute(text("ALTER TABLE courses ADD COLUMN source_language_id INTEGER"))
        if "target_language_id" not in columns:
            connection.execute(text("ALTER TABLE courses ADD COLUMN target_language_id INTEGER"))

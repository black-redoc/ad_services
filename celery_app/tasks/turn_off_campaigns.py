from celery_app.celery import app
from sqlalchemy import (
    Table,
    update,
    create_engine,
    String,
    Integer,
    Boolean,
    MetaData,
    Column,
)
import os
import dotenv

dotenv.load_dotenv()

DB_CONNECTION = os.environ.get("DB_CONNECTION")

engine = create_engine(
    DB_CONNECTION,
    pool_size=5,
    max_overflow=1,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
    echo=True,
)
metadata = MetaData()

Campaign = Table(
    "campaign",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
    ),
    Column("current_spent_budget", Integer, nullable=False),
    Column("budget_limit", Integer, nullable=False),
    Column("is_active", Boolean, default=True),
    Column("budget_kind", String(7), nullable=False),
)


@app.task
def turn_off_campaigns(id: int):
    with engine.connect() as conn:
        stmt = update(Campaign).where(Campaign.c.id == id).values(is_active=False)
        result = conn.execute(stmt)
        print(f"{result.rowcount} rows affected.")
        conn.commit()
    engine.dispose()

import random
from celery_app.celery import app
from sqlalchemy import (
    Table,
    Integer,
    Column,
    String,
    Boolean,
    MetaData,
    create_engine,
    update,
    select,
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
def budget_consumer():
    with engine.connect() as conn:
        rd_number = random.randint(1, 4)

        query = select(Campaign).where(
            Campaign.c.id == rd_number,
            Campaign.c.is_active == True,
        )
        campaign = conn.execute(query).fetchone()
        if campaign is None:
            engine.dispose()
            print("No campaign found")
            return
        budget_increment = random.randint(1, 10)
        stmt = (
            update(Campaign)
            .where(
                Campaign.c.id == rd_number,
                Campaign.c.is_active == True,
            )
            .values(
                current_spent_budget=campaign.current_spent_budget + budget_increment
            )
        )
        result = conn.execute(stmt)
        print(f"{result.rowcount} rows updated.")
        conn.commit()
    engine.dispose()

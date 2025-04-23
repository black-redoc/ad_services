from celery_app.celery import app
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    Boolean,
    String,
    update,
    and_,
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


def execute_query(budget_kind: str, conn):
    # run queries for each budget_kind (daily, monthly)
    stmt = (
        update(Campaign)
        .where(
            and_(Campaign.c.is_active == False, Campaign.c.budget_kind == budget_kind)
        )
        .values(is_active=True, current_spent_budget=0)
    )
    result = conn.execute(stmt)
    print(f"{result.rowcount} rows affected.")
    conn.commit()


@app.task
def turn_on_campaigns_daily():
    # only run daily, at midnight
    with engine.connect() as conn:
        execute_query("daily", conn)
    engine.dispose()


@app.task
def turn_on_campaigns_monthly():
    # only run monthly, the first day of the month at midnight
    with engine.connect() as conn:
        execute_query("monthly", conn)
    engine.dispose()

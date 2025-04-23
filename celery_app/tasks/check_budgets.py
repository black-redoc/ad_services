from celery_app.celery import app
from sqlalchemy import (
    Table,
    MetaData,
    String,
    Integer,
    Boolean,
    create_engine,
    Column,
    select,
    and_,
)
import os
import dotenv

dotenv.load_dotenv()

DB_CONNECTION = os.environ.get("DB_CONNECTION")
print(DB_CONNECTION)
engine = create_engine(
    DB_CONNECTION,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
    echo=True,
)

metadata = MetaData()
Campaign = Table(
    "campaign",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("current_spent_budget", Integer, nullable=False),
    Column("budget_limit", Integer, nullable=False),
    Column("is_active", Boolean, default=True),
    Column("budget_kind", String, nullable=False),
)


@app.task
def check_budgets():
    with engine.connect() as conn:
        # get just the active campaigns
        # and check if they are over budget
        query = select(Campaign).where(
            and_(
                Campaign.c.is_active == True,
                Campaign.c.current_spent_budget >= Campaign.c.budget_limit,
            )
        )
        result = conn.execute(query).fetchall()
        # if there are any over budget campaigns, turn them off
        for row in result:
            id = row[0]
            app.send_task(
                "celery_app.tasks.turn_off_campaigns.turn_off_campaigns", args=[id]
            )

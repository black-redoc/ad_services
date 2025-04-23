#!/usr/bin/env python3
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    Boolean,
    String,
    insert,
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

campaigns = [
    {"id": 1, "current_spent_budget": 0, "budget_limit": 100, "budget_kind": "daily"},
    {"id": 2, "current_spent_budget": 0, "budget_limit": 100, "budget_kind": "monthly"},
    {"id": 3, "current_spent_budget": 0, "budget_limit": 100, "budget_kind": "daily"},
    {"id": 4, "current_spent_budget": 0, "budget_limit": 100, "budget_kind": "mothly"},
]


def main():
    metadata.create_all(engine)
    with engine.connect() as connection:
        connection.execute(insert(Campaign), campaigns)
        connection.commit()

    engine.dispose()


if __name__ == "__main__":
    main()

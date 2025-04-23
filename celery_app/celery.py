from celery import Celery
import dotenv
import os

dotenv.load_dotenv()

REDIS_URL = os.environ.get("REDIS_URL")

app = Celery(
    "budget_campaigns",
    broker=REDIS_URL,
    result_backend=REDIS_URL,
)

app.autodiscover_tasks(["celery_app.tasks"])

app.conf.beat_schedule = {
    "check_budget": {
        "task": "celery_app.tasks.check_budgets.check_budgets",
        "schedule": 10.0,  # simulate an hour
    },
    "turn_on_campaigns_daily": {
        "task": "celery_app.tasks.turn_on_campaigns.turn_on_campaigns_daily",
        "schedule": 60.0,  # simulate a day
    },
    "turn_on_campaigns_monthly": {
        "task": "celery_app.tasks.turn_on_campaigns.turn_on_campaigns_monthly",
        "schedule": 80.0,  # simulate a month
    },
    "budget_consumer": {
        "task": "celery_app.tasks.budget_consumer.budget_consumer",
        "schedule": 10.0,  # simulate an hour
    },
}

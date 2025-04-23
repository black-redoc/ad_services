# ADs Management System

This is a microservice architecture that manage asyncrunously the updating and checking of the
daily/monthly budget per campaign in an agency.


## How to run it locally:

### 1. Start docker-compose

```bash
docker-compose up
```

### 2. Install the dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup the database

```bash
python setup.py
```

### 4. Run the celery worker

```bash
celery -A celery_app.celery worker -l info
```

### 5. Run the celery beat

```bash
celery -A celery_app.celery beat -l info
```

### 6. Go to http://localhost:8080 and check the database

```text
Login with
- Username: postgres
- Password: secret
- Database: postgres
```

## Structure

- campaigns table

| id | current_spent_budget | budget_limit | is_active | budget_kind |
|----|----------------------|-------------|-----------|-------------|
| 1  | 0                    | 100         | True      | daily       |
| 2  | 0                    | 100         | True      | monthly     |
| 3  | 0                    | 100         | True      | daily       |
| 4  | 0                    | 100         | True      | monthly     |

## Asumptions

- The campaings table are checked/updated  every 10 seconds simulating an hour
- The campaigns table is updated every 60 seconds simulating the turn on of campaigns daily
- The campaigns table is updated every 120 seconds simulating the turn on of campaigns monthly
- The campaigns table is updated every 10 seconds simulating the budget_consumer task, like user views in a campaign

## The flow of the system

1. The user views a campaigns simulated by the budget_consumer task
2. There' a check_budget task that checks if the campaign is over budget
3. If the campaign is over budget, the turn_off_campaigns task turns the campaign off
4. The turn_on_campaigns_daily task turns the campaign on
5. The turn_on_campaigns_monthly task turns the campaign on

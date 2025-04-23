# Application Logic

Application to manage the AD budgets of the agencies which have ad campaigns and have a limt of use per day/month.


- Checking and updating daily/monthly spends


## Services:


```python
# check_update_budget
EACH 60 MINUTES DO:
GET budgets_per_campaigns From DataSource

FOR EACH budget IN budgets_per_campaigns:
    IF butget.current_budget >= budget.limit_budget:
        CALL: turn_off_ads budget.id
```


```python
# turn_off_ads RECEIVES campaign_id

GET campaing BY campaign_id FROM DataSource

campaign.is_active = FALSE

UPDATE campaign IN DataSource
```


```python
# check turn_on
EACH DAY AT 0 HOURS AND 0 SECONDS DO:

GET budgets_per_campaigns FROM DataSource

FOR EACH budget IN budgets_per_campaigns:
    IF budget.current_budget < budget.limit AND  budget.is_active = FALSE:
        CALL: turn_on_ads budget.id
```


```python
# turn_on_ads RECEIVES campaign_id
GET campaign BY campaign_id FROM DataSource

campaign.is_active = TRUE

UPDATE campaign IN DataSource
```


FastAPI reporting service for FarmHub

This small service connects to the existing SQLite database used by the Django `core/` service and provides read-only aggregated endpoints.

How it works
- Uses SQLModel (SQLAlchemy) to reflect minimal tables required for reporting: User, Farm, Cow, MilkRecord, Activity.
- Connects to the `core/db.sqlite3` file by default.

Endpoints
- GET /farms/{farm_id}/summary - returns number of farmers, cows, and total milk produced
- GET /milk - query by farm_id, farmer_id, start_date, end_date
- GET /activities/recent - returns recent activities

Run locally (from reporting/):

    pip install -r requirements.txt
    uvicorn main:app --reload --host 127.0.0.1 --port 8001

Notes
- Read-only service. No migrations or writes.

from fastapi import FastAPI, Query, HTTPException
from sqlmodel import Session, create_engine, select, func
from sqlalchemy.exc import OperationalError
from typing import Optional, List
from datetime import date
import os
from pathlib import Path

from models import User, Cow, MilkRecord, Activity


DATABASE_URL = "sqlite:///../core/db.sqlite3"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

app = FastAPI(title='FarmHub Reporting')


@app.get('/health')
def health():
    return {'status': 'ok'}


@app.get('/farms/{farm_id}/summary')
def farm_summary(farm_id: int):
    with Session(engine) as session:
        # number of farmers (users who own cows at the farm)
        farmer_count = session.exec(
            select(func.count(func.distinct(User.id))).join(Cow, Cow.owner_id == User.id).where(Cow.farm_id == farm_id)
        ).one()

        cow_count = session.exec(select(func.count(Cow.id)).where(Cow.farm_id == farm_id)).one()

        total_milk = session.exec(
            select(func.coalesce(func.sum(MilkRecord.quantity_liters), 0)).join(Cow, Cow.id == MilkRecord.cow_id).where(Cow.farm_id == farm_id)
        ).one()

    return {
        'farm_id': farm_id,
        'farmer_count': int(farmer_count or 0),
        'cow_count': int(cow_count or 0),
        'total_milk_liters': float(total_milk or 0),
    }


@app.get('/milk')
def milk_records(farm_id: Optional[int] = None, farmer_id: Optional[int] = None, start_date: Optional[date] = None, end_date: Optional[date] = None, limit: int = 100):
    with Session(engine) as session:
        q = select(MilkRecord, Cow, User).join(Cow, Cow.id == MilkRecord.cow_id).join(User, User.id == MilkRecord.recorded_by_id)
        if farm_id:
            q = q.where(Cow.farm_id == farm_id)
        if farmer_id:
            q = q.where(MilkRecord.recorded_by_id == farmer_id)
        if start_date:
            q = q.where(MilkRecord.date >= start_date)
        if end_date:
            q = q.where(MilkRecord.date <= end_date)
        q = q.limit(limit)

        rows = session.exec(q).all()

        results = []
        for mr, cow, user in rows:
            results.append({
                'id': mr.id,
                'cow_id': cow.id,
                'cow_tag': cow.tag,
                'farm_id': cow.farm_id,
                'recorded_by': user.id if user else None,
                'recorded_by_username': user.username if user else None,
                'date': mr.date.isoformat(),
                'quantity_liters': float(mr.quantity_liters),
            })

    return results


@app.get('/activities/recent')
def recent_activities(limit: int = 50):
    with Session(engine) as session:
        q = select(Activity, Cow, User).join(Cow, Cow.id == Activity.cow_id).join(User, User.id == Activity.performed_by_id).order_by(Activity.date.desc()).limit(limit)
        rows = session.exec(q).all()
        out = []
        for act, cow, user in rows:
            out.append({
                'id': act.id,
                'cow_id': cow.id,
                'cow_tag': cow.tag,
                'farm_id': cow.farm_id,
                'performed_by': user.id if user else None,
                'performed_by_username': user.username if user else None,
                'activity_type': act.activity_type,
                'notes': act.notes,
                'date': act.date.isoformat(),
            })
    return out

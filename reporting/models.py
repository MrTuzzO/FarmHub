from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import datetime


class User(SQLModel, table=True):
    __tablename__ = 'accounts_user'
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: Optional[str]
    role: Optional[str]


class Farm(SQLModel, table=True):
    __tablename__ = 'farms_farm'
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    location: Optional[str]
    agent_id: Optional[int]


class Cow(SQLModel, table=True):
    __tablename__ = 'cows_cow'
    id: Optional[int] = Field(default=None, primary_key=True)
    tag: str
    breed: Optional[str]
    farm_id: int
    owner_id: Optional[int]
    dob: Optional[datetime.date]


class MilkRecord(SQLModel, table=True):
    __tablename__ = 'milk_milkrecord'
    id: Optional[int] = Field(default=None, primary_key=True)
    cow_id: int
    recorded_by_id: Optional[int]
    date: datetime.date
    quantity_liters: float


class Activity(SQLModel, table=True):
    __tablename__ = 'activities_activity'
    id: Optional[int] = Field(default=None, primary_key=True)
    cow_id: int
    performed_by_id: Optional[int]
    activity_type: Optional[str]
    notes: Optional[str]
    date: datetime.date

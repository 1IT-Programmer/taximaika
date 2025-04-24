from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    trips: list = []

    class Config:
        orm_mode = True

class TripBase(BaseModel):
    departure_point: str
    arrival_point: str
    distance: float
    cost: float

class TripCreate(TripBase):
    pass

class Trip(TripBase):
    id: int
    timestamp: datetime
    owner_id: int

    class Config:
        orm_mode = True

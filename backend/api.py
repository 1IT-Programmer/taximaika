from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import User, Trip
from .schemas import UserCreate, TripCreate
from .auth import get_current_user
from .config import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from passlib.context import CryptContext

app = FastAPI()


# Настройка поддержки статических ресурсов
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Рендеринг шаблонов
templates = Jinja2Templates(directory="frontend/templates")

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Подключение к базе данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Роут для регистрации пользователя
@app.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = CryptContext(schemes=["bcrypt"]).hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password, full_name=user.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Роут для создания новой поездки
@app.post("/trips/", response_model=TripCreate)
def create_trip(trip: TripCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_trip = Trip(**trip.dict(), owner_id=current_user.id)
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip

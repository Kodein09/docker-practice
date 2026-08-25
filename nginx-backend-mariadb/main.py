import os
from contextlib import asynccontextmanager
from tkinter.font import names

from pydantic import BaseModel

from fastapi import FastAPI, HTTPException
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DB_PORT = os.getenv("DB_PORT")
DB_HOST = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PASS")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}/{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_async_engine(url=DATABASE_URL, echo=True)
AsyncLocalSession = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(50), unique=True)
    password = Column(String(100))


class UserSchema(BaseModel):
    name: str
    email: str
    password: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

@app.post('/create')
async def create_user(user_data: UserSchema) -> dict:
    async with AsyncLocalSession() as session:
        new_user = Users(
            name=user_data.name,
            email=user_data.email,
            password=user_data.password
        )
        session.add(new_user)
        try:
            await session.commit()
            return {"status": "success"}
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Error creating user (email might already exist)")

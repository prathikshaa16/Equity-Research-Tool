from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..core.config import settings

# SQLAlchemy Database
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# MongoDB Connection
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

# Async MongoDB client
async_mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
async_mongo_db = async_mongo_client.equity_ai

# Sync MongoDB client for simple operations
mongo_client = MongoClient(settings.MONGODB_URL)
mongo_db = mongo_client.equity_ai


async def get_mongo_db():
    return async_mongo_db


def get_sync_mongo_db():
    return mongo_db

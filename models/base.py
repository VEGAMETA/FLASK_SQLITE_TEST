from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from main import app

db = SQLAlchemy(app)
async_engine = create_async_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True, future=True)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

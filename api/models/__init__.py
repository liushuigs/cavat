from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declarative_base
from configs import config

Base = declarative_base()

engine = create_engine(
        config.DATABASE_URI, pool_recycle=3600)
Base.metadata.bind = engine
session_factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
session = scoped_session(session_factory)

__all__ = [Base, session]
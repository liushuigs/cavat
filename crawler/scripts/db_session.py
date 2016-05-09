from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from base import Base


class DBSession(object):

    @staticmethod
    def get_db_session(mysql_uri):
        engine = create_engine(
                mysql_uri, pool_recycle=3600, encoding='utf-8')
        Base.metadata.bind = engine
        session_factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
        return scoped_session(session_factory)

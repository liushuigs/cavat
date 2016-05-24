import datetime
from . import Base, session
from sqlalchemy import Column, Integer, TIMESTAMP, String, SMALLINT, TEXT, Boolean


class RawData(Base):
    __tablename__ = 'raw_data'

    id = Column(Integer, primary_key=True)
    created_ts = Column(TIMESTAMP())
    updated_ts = Column(TIMESTAMP())
    domain = Column(String(100))
    url = Column(String(255))
    depth = Column(SMALLINT)
    http_status = Column(String(3))
    html = Column(TEXT())
    parsed_as_entry = Column(Boolean())

    def extend(self, data):
        for key in data:
            setattr(self, key, data[key])

    @staticmethod
    def create(**kwargs):
        url = kwargs.get('url')
        now_date = datetime.datetime.utcnow()
        record = session.query(RawData). \
            filter(RawData.url == url).first()
        if record is None:
            record = RawData(created_ts=now_date,
                             updated_ts=now_date)
            action = 'insert'
        else:
            record.updated_ts = now_date
            action = 'update'
        record.extend(kwargs)
        try:
            session.add(record)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return action

    @staticmethod
    def create_entry(**kwargs):
        url = kwargs.get('url')
        record = session.query(RawData). \
            filter(RawData.url == url).first()
        if record is not None:
            return
        RawData.create(**kwargs)


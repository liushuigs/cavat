import datetime
from base import Base
from sqlalchemy import Column, Integer, TIMESTAMP, String


class Domain(Base):
    __tablename__ = 'domain'

    id = Column(Integer, primary_key=True)
    domain = Column(String(100))
    spider_name = Column(String(60))
    article_num = Column(Integer())
    created_ts = Column(TIMESTAMP())
    updated_ts = Column(TIMESTAMP())

    @staticmethod
    def create(session, domain, spider_name, article_num=None):
        now_date = datetime.datetime.utcnow()
        record = session.query(Domain).\
            filter_by(domain=domain).first()
        if record is None:
            record = Domain(domain=domain,
                            spider_name=spider_name,
                            article_num=article_num,
                            created_ts=now_date,
                            updated_ts=now_date)
        else:
            record.domain
            record.spider_name = spider_name
            record.article_num = article_num
            record.updated_ts = now_date
        session.add(record)
        session.commit()

        return record

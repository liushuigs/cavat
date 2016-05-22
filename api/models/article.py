from sqlalchemy import func
from . import Base, session
from sqlalchemy import Column, Integer, TIMESTAMP, String, Text
from datetime import datetime


class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    url = Column(String(25))
    title = Column(String(255))
    content = Column(Text)
    created_ts = Column(TIMESTAMP)
    url = Column(String(255))

    @staticmethod
    def count(domain, today=False):
        """
        speed up sqlalchemy count
        docs https://gist.github.com/hest/8798884
        :param domain:
        :param today: just count today's new articles
        :return:
        """
        q = session.query(Article). \
            filter(Article.url.like("%" + domain + "%"))
        if today is True:
            now_date = datetime.utcnow()
            now_date = now_date.strftime('%Y-%m-%d 00:00:00')
            q = q.filter(Article.created_ts > now_date)
        count_q = q.statement.with_only_columns([func.count()]).order_by(None)
        return q.session.execute(count_q).scalar()

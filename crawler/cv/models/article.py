from sqlalchemy import func
from cv.models import Base, session
from sqlalchemy import Column, Integer, TIMESTAMP, String, Text


class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    url = Column(String(25))
    title = Column(String(255))
    content = Column(Text)
    created_ts = Column(TIMESTAMP)
    url = Column(String(255))

    @staticmethod
    def count(domain):
        """
        speed up sqlalchemy count
        docs https://gist.github.com/hest/8798884
        :param domain:
        :return:
        """
        q = session.query(Article). \
            filter(Article.url.like("%" + domain + "%"))
        count_q = q.statement.with_only_columns([func.count()]).order_by(None)
        return q.session.execute(count_q).scalar()

    @staticmethod
    def check_exists(link):
        record = session.query(Article).\
            filter(Article.url == link)
        return record is not None

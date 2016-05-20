from . import Base, session
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
    def get_all():
        data = session.query(Domain).all()
        return [item.serialize for item in data]

    @property
    def serialize(self):
        """
        docs: http://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask
        :return:
        """
        return {
            'domain': self.domain,
            'article_num': self.article_num,
            'created_ts': self.created_ts,
            'updated_ts': self.updated_ts
        }

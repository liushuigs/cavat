# -*- coding: utf-8 -*-

# from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, create_engine
from cv.models import db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义article对象:
class Article(Base):
    # 表的名字:
    __tablename__ = 'article'

    # 表的结构:
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(25))
    title = db.Column(db.String(225))
    content = db.Column(db.Text)
    created_ts = db.Column(db.TIMESTAMP)

    def get_one(self, id):
        # 初始化数据库连接:
        engine = db.create_engine('mysql+pymysql://root:123456@localhost/cavat?charset=utf8')
        # 创建DBSession类型:
        DBSession = sessionmaker(bind=engine)
        # 创建Session:
        session = DBSession()
        # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
        article = session.query(self.__class__).filter(self.__class__.id == id).one()
        # 打印类型和对象的name属性:
        print 'type:', type(article)
        print 'url:', article.content
        # 关闭Session:
        session.close()

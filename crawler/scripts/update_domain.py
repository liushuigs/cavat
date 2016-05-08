from scripts.db_session import DBSession
from configs import config
from cv.models.domain import Domain
from cv.models.article import Article


def update_table():
    """
    init or update domain table
    :return:
    """
    session = DBSession.get_db_session(config.DATABASE_URI)
    data = [
        {"domain": '36kr.com', "spider_name": '36kr'},
        {"domain": 'huxiu.com', "spider_name": 'huxiu'},
        {"domain": 'iheima.com', "spider_name": 'iheima'},
        {"domain": 'medium.com', "spider_name": 'medium'},
        {"domain": 'pedaily.cn', "spider_name": 'pedaily'},
        {"domain": 'startup-partner.com', "spider_name": 'startup-partner'},
        {"domain": 'techcrunch.com', "spider_name": 'techcrunch'},
        {"domain": 'thenextweb.com', "spider_name": 'thenextweb'},
        {"domain": 'tmtpost.com', "spider_name": 'tmt'},
        {"domain": 'venturebeat.com', "spider_name": 'venturebeat'},
    ]
    for spider in data:
        article_num = Article.count(session, spider["domain"])
        Domain.create(session, article_num=article_num, **spider)

if __name__ == '__main__':
    update_table()

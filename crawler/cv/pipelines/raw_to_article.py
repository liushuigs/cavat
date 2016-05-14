import re
import logging
from cv.models.raw_data import RawData
from cv.models import session
from scrapy.selector import Selector
from cv.pipelines.medium import parse_html
from cv.pipelines.article import ArticlePipeline
article = ArticlePipeline()
logger = logging.getLogger(__name__)


def raw_to_article():
    data = session.query(RawData).\
        filter(RawData.depth == 6).\
        filter(RawData.http_status == '200').\
        filter(RawData.html is not None).\
        offset(70000).limit(10000).all()
    num = 0
    for record in data:
        if re.compile('.*medium.com\/@?.*\/.*').match(str(record.url)) is not None:
            # TODO remove source= from url ? should confirm
            html = record.html
            response = Selector(text=html)
            url = remove_params(record.url)
            if url != record.url:
                print url
            item = parse_html(response, url=str(url))
            if item:
                article.insert(item, logger=logger)
                print record.url
                num += 1
    print 'success ' + str(num)


def remove_params(url):
    question_mark_position = url.find('?')
    if question_mark_position > -1:
        return url[:question_mark_position]
    else:
        return url

if __name__ == '__main__':
    raw_to_article()

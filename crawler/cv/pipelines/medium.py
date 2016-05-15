import datetime
import re
from cv.items.article import ArticleItem
from ..util.time import datetime_str_to_utc


def parse_html(response, url=None):
    """
    TODO lang="ja"
    :param response:
    :param url:
    :return:
    """
    item = ArticleItem()
    now_date = datetime.datetime.utcnow()
    now_date = now_date.strftime('%Y-%m-%d %H:%M:%S')
    published_ts = response.xpath('//meta[@property="article:published_time"]/@content').extract_first()
    if published_ts is None:
        return item
    time_str = published_ts[:19].replace('T', ' ')
    timezone = -7
    published_ts = datetime_str_to_utc(time_str, timezone)
    source_type = response.css('.postArticle--full').xpath('//@lang').extract_first()

    item['url'] = url if url is not None else response.url
    item['title'] = response.xpath('//title/text()').extract_first()
    item['content'] = response.css('.postArticle-content').extract_first()
    item['summary'] = None
    item['published_ts'] = published_ts
    item['created_ts'] = now_date
    item['updated_ts'] = now_date
    item['time_str'] = None
    item['author_name'] = response.xpath('//meta[@name="author"]/@content').extract_first()
    item['author_link'] = response.xpath('//meta[@property="article:author"]/@content').extract_first()
    item['author_avatar'] = None
    item['tags'] = None
    item['site_unique_id'] = None
    item['author_id'] = 0
    item['author_email'] = None
    item['author_phone'] = None
    item['author_role'] = None
    item['cover_real_url'] = None
    item['source_type'] = source_type
    item['views_count'] = 0
    item['cover'] = None
    return item


black_list = [
    # 200, but useless
    '.*redirect=.*',
    # 302
    '.*_/vote/p/.*',
    # 302
    '.*_/bookmark/p/.*',
    # 302
    '.*_/subscribe/.*',
    # 301
    '.*medium.com/p/\w+$',
    # 404
    '.*medium.com/story-unbound.*',
    '.*above-average.*',
]

__all__ = [parse_html, black_list]

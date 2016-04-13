import datetime
import json
import os
from os.path import dirname
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from cv.items.article import ArticleItem


def parse_from_file():
    filename = os.path.abspath(__file__)
    with open(dirname(dirname(filename)) + '/data/5045706.html', 'r') as f:
        target = Selector(text=f.read())

    obj = target.css('.js-react-on-rails-component')\
        .xpath('@data-props').extract()
    result = json.loads(obj[0])
    post = result['data']['post']

    item = ArticleItem()
    item['url'] = result['data']['router']
    item['title'] = post['title']
    item['content'] = post['display_content']
    item['summary'] = post['summary']
    item['published_ts'] = post['published_at']
    item['created_ts'] = datetime.datetime.utcnow()
    item['updated_ts'] = datetime.datetime.utcnow()
    item['time_str'] = result['data']['router']
    item['author_name'] = post['author']['display_name']
    item['author_link'] = post['author']['domain_path']
    item['author_avatar'] = post['author']['avatar']
    item['tags'] = post['display_tag_list']
    print item


def parse_body():
    pass


def parse_from_url():
    # TODO http://doc.scrapy.org/en/master/topics/selectors.html#topics-selectors
    pass


if __name__ == '__main__':
    parse_from_file()
    # parse_from_url()

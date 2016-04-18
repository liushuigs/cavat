# -*- coding: utf-8 -*-
import datetime
import json
import scrapy
from cv.items.article import ArticleItem
from urlparse import urljoin


class A36krSpider(scrapy.Spider):
    name = "36kr"
    allowed_domains = ["36kr.com"]
    start_urls = (
        'http://36kr.com/p/5045706.html',
    )

    def parse(self, response):
        # filename = 'data/'+response.url.split("/")[-1]
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        obj = response.css('.js-react-on-rails-component') \
            .xpath('@data-props').extract()
        result = json.loads(obj[0])
        post = result['data']['post']

        nowdate = datetime.datetime.utcnow()
        nowdate = nowdate.strftime('%Y-%m-%d %H:%M:%S')
        domain = 'http://36kr.com'
        item = ArticleItem()
        item['url'] = urljoin(domain, result['data']['router'])
        item['title'] = post['title']
        item['content'] = post['display_content']
        item['summary'] = post['summary']
        item['published_ts'] = self.datetime_str_to_utc(post['published_at'])
        item['created_ts'] = nowdate
        item['updated_ts'] = nowdate
        item['time_str'] = ''
        item['author_name'] = post['author']['display_name']
        item['author_link'] = urljoin(domain, post['author']['domain_path'])
        item['author_avatar'] = post['author']['avatar']
        item['tags'] = ','.join(post['display_tag_list'])
        # print item
        yield item

    @staticmethod
    def datetime_str_to_utc(date_str):
        dt = datetime.datetime.strptime(date_str[:19], "%Y-%m-%dT%H:%M:%S")
        ds = dt - datetime.timedelta(hours=8)
        return ds.strftime('%Y-%m-%d %H:%M:%S')

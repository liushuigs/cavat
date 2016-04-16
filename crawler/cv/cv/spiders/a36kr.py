# -*- coding: utf-8 -*-
import scrapy
import datetime
import json
from cv.items.article import ArticleItem

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
        obj = response.css('.js-react-on-rails-component')\
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
        # print item
        yield item
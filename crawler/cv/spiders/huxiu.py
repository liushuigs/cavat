# -*- coding: utf-8 -*-
import scrapy
from cv.items.article import ArticleItem


class HuxiuSpider(scrapy.Spider):
    name = "huxiu"
    allowed_domains = ["huxiu.com"]
    start_urls = (
        #'http://www.huxiu.com/',
        'http://www.huxiu.com/article/146942',
    )
    #custom_settings = {
    #    'ITEM_PIPELINES': {
    #        'cv.pipelines.a36kr.ArticlePipeline': 300
    #    }
    #}

    def parse(self, response):
        item = ArticleItem()
        sel = response.selector

        print 'start'.center(100, '=')
        item['url'] = response.url
        item['title'] = sel.xpath('//title/text()').extract()[0]
        item['content'] = sel.css('#article_content').extract()[0]
        item['summary'] = None
        item['published_ts'] = None
        item['created_ts'] = None
        item['updated_ts'] = None
        item['time_str'] = None
        item['author_name'] = None
        item['author_link'] = None
        item['author_avatar'] = None
        item['tags'] = None
        item['site_unique_id'] = None
        item['author_id'] = None
        item['author_email'] = None
        item['author_phone'] = None
        item['author_role'] = None
        item['cover_real_url'] = None
        item['source_type'] = None
        item['views_count'] = None
        item['cover'] = None
        print item.get('url')
        print 'end'.center(100, '=')
        yield item

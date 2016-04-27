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
    custom_settings = {
        'ITEM_PIPELINES': {
            'cv.pipelines.a36kr.ArticlePipeline': 300
        }
    }

    def parse(self, response):
        print 'start'.center(100, '=')
        item = self.parse_page(response)
        print item['author_link']
        print 'end'.center(100, '=')
        yield item

    def parse_page(self, response):
        sel = response.selector
        item = ArticleItem()
        item['url'] = response.url
        item['title'] = sel.xpath('//title/text()').extract()[0]
        item['content'] = sel.css('#article_content').extract()[0]
        item['summary'] = None
        item['published_ts'] = None
        item['created_ts'] = None
        item['updated_ts'] = None
        item['time_str'] = None
        item['author_name'] = sel.css('.box-author-info').css('.author-name a::text').extract()[0]
        item['author_link'] = sel.css('.box-author-info').css('.author-name a::attr(href)').extract()[0]
        item['author_avatar'] = sel.css('.box-author-info').css('.author-face img::attr(src)').extract()[0]
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
        return item

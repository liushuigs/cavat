# -*- coding: utf-8 -*-
from datetime import datetime
from os.path import splitext, basename

import re
import scrapy
from ..items.article import ArticleItem
from ..util.time import datetime_str_to_utc


class GurongeSpider(scrapy.Spider):
    name = "guronge"
    allowed_domains = ["guronge.com"]
    custom_settings = {
        'DOWNLOAD_DELAY': 0.15,
        # 'CONCURRENT_REQUESTS': 15,
        'ITEM_PIPELINES': {
            'cv.pipelines.article.ArticlePipeline': 300
        }
    }

    max_article_page = 60
    current_num = 1
    current_task = None

    def __init__(self, task=None, **kwargs):
        super(GurongeSpider, self).__init__(**kwargs)
        current_num = str(self.current_num)
        if task == 'home':
            url = ['http://www.guronge.com']
        elif task == 'single':
            url = (
                'http://www.guronge.com/p/1527.html',
            )
        elif task == 'onepage':
            url = ['http://www.guronge.com/content/b/itemid/32/t/columns/p/1']
        elif task == 'pages':
            url = (
                'http://www.guronge.com/content/b/itemid/32/t/columns/p/'+current_num,
            )
        else:
            self.logger.error('Parameter Error!')
            return
        self.start_urls = url
        self.current_task = task

    def parse(self, response):
        task = self.current_task

        if task == 'single':
            yield self.parse_item(response)

        # parse homepage for update
        if task == 'home':
            lists = self.parse_homepage_links(response)
            cnt = 0
            for link in lists:
                yield scrapy.Request(link, callback=self.parse_item)
                cnt += 1
            self.logger.info('[parse homepage for update][total articles: %d]', cnt)

        # parse a specific page
        if task == 'onepage':
            lists = self.parse_article_links(response)
            for link in lists:
                yield scrapy.Request(link, callback=self.parse_item)
            self.logger.info('[parse a specific page] %s', response.url)

        # parse multiple pages
        if task == 'pages':
            lists = self.parse_article_links(response)
            for link in lists:
                yield scrapy.Request(link, callback=self.parse_item)
            if self.current_num <= self.max_article_page:
                self.current_num += 1
                next_page_url = re.sub(r'columns/p/\d+$', 'columns/p/'+str(self.current_num), response.url)
                yield scrapy.Request(next_page_url)

    @staticmethod
    def parse_homepage_links(response):
        lists = response.xpath('//a/@href').extract()
        lists = [x for x in lists if re.compile('.*guronge.*/p/\d+\.html').match(x)]
        lists = set(lists)
        return lists

    @staticmethod
    def parse_article_links(response):
        lists = response.css('.index-left').xpath('.//a/@href').extract()
        lists = [x for x in lists if re.compile('.*guronge.*/p/\d+\.html').match(x)]
        lists = set(lists)
        return lists

    @staticmethod
    def parse_item(response):
        now_date = datetime.utcnow()
        now_date = now_date.strftime('%Y-%m-%d %H:%M:%S')
        published_ts = None

        item = ArticleItem()
        item['url'] = response.url
        title = response.css('.box-header .title::text').extract_first()
        item['title'] =  title if title else response.xpath('//title/text()').extract_first()
        item['content'] = ''.join( response.css('.box-content').xpath('./p').extract())
        item['summary'] = response.xpath('//meta[@name="description"]/@content').extract_first()
        item['published_ts'] = published_ts
        item['created_ts'] = now_date
        item['updated_ts'] = now_date
        item['time_str'] = None
        item['author_name'] = response.css('.box-header .author::text').extract_first()
        item['author_link'] = None
        item['author_avatar'] = None
        item['tags'] = response.xpath('//meta[@name="keywords"]/@content').extract_first()
        item['site_unique_id'] = splitext(basename(response.url))[0]
        item['author_id'] = 0
        item['author_email'] = None
        item['author_phone'] = None
        item['author_role'] = None
        item['cover_real_url'] = None
        item['source_type'] = None
        item['views_count'] = 0
        item['cover'] = None
        return item

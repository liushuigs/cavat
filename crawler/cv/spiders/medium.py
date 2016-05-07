# -*- coding: utf-8 -*-
import datetime
import re
import scrapy
from cv.items.article import ArticleItem
from ..util.time import datetime_str_to_utc


class MediumSpider(scrapy.Spider):
    name = "medium"
    allowed_domains = ["medium.com"]
    start_urls = (
        'https://medium.com',
        # 'https://medium.com/browse/b99480981476',
    )
    custom_settings = {
        'DOWNLOAD_DELAY': 0.80,
        'DOWNLOAD_TIMEOUT': 6,
        'AUTOTHROTTLE_ENABLED': True,
        # 'AUTOTHROTTLE_DEBUG': True,
        'CONCURRENT_REQUESTS': 13, # equals article numbers in each page plus 1
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'ITEM_PIPELINES': {
            'cv.pipelines.article.ArticlePipeline': 300
        }
    }

    def parse(self, response):
        # parse homepage for update
        domain = 'https://medium.com'
        # find tech link from hompage
        if response.url == domain:
            tech_url = response.css('.browsableStreamTabs').xpath('//a[text()="Technology"]/@href').extract_first()
            self.logger.info('[find list] %s', tech_url)
            yield scrapy.Request(tech_url)
        # parse tech list page
        if response.url.find('/browse/') != -1:
            lists = self.get_article_links(response)
            for link in lists:
                yield scrapy.Request(link, callback=self.parse_page)

        # TODO parse multiple pages

        # parse a single article
        if re.compile('.*medium.com\/@.*\/.*').match(response.url) is not None:
            item = self.parse_page(response)
            yield item

    @staticmethod
    def get_article_links(response):
        lists = response.xpath('//a/@href').extract()
        lists = [x for x in lists if re.compile('.*medium.com\/@[^/]*\/[^/]*$').match(x)]
        lists = list(set(lists))
        return lists

    @staticmethod
    def parse_page(response):
        now_date = datetime.datetime.utcnow()
        now_date = now_date.strftime('%Y-%m-%d %H:%M:%S')
        published_ts = response.xpath('//meta[@property="article:published_time"]/@content').extract_first()
        time_str = published_ts[:19].replace('T', ' ')
        timezone = -7
        published_ts = datetime_str_to_utc(time_str, timezone)

        item = ArticleItem()
        item['url'] = response.url
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
        item['source_type'] = None
        item['views_count'] = 0
        item['cover'] = None
        return item

# -*- coding: utf-8 -*-
import datetime
import re
import scrapy
from cv.models.article import Article
from cv.pipelines.medium import parse_html


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
        'CONCURRENT_REQUESTS': 13,  # equals article numbers in each page plus 1
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
            lists = self.get_article_links(response)
            for link in lists:
                if Article.check_exists(link) is False:
                    yield scrapy.Request(link, callback=self.parse_page)

        # parse a single article
        if re.compile('.*medium.com\/@.*\/.*').match(response.url) is not None:
            item = self.parse_page(response)
            yield item

    @staticmethod
    def get_article_links(response):
        lists = response.xpath('//a/@href').extract()
        lists = [MediumSpider.remove_params(x) for x in lists if
                 re.compile('.*medium.com\/@[^/]*\/[^/]*$').match(x)]
        lists = list(set(lists))
        return lists

    @staticmethod
    def remove_params(link):
        question_mark = link.find('?')
        if question_mark > -1:
            link = link[:question_mark]
        hash_pos = link.find('#')
        if hash_pos > -1:
            link = link[:hash_pos]
        return link

    @staticmethod
    def parse_page(response):
        return parse_html(response)

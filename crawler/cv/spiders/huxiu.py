# -*- coding: utf-8 -*-
import scrapy


class HuxiuSpider(scrapy.Spider):
    name = "huxiu"
    allowed_domains = ["huxiu.com"]
    start_urls = (
        'http://www.huxiu.com/',
    )

    def parse(self, response):
        pass

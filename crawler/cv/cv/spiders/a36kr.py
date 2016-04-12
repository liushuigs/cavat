# -*- coding: utf-8 -*-
import scrapy


class A36krSpider(scrapy.Spider):
    name = "36kr"
    allowed_domains = ["36kr.com"]
    start_urls = (
        'http://36kr.com/p/5045706.html',
    )

    def parse(self, response):
        filename = 'data/'+response.url.split("/")[-1]
        with open(filename, 'wb') as f:
            f.write(response.body)

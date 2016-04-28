# -*- coding: utf-8 -*-
import datetime
import json
import re
import scrapy
from cv.items.article import ArticleItem
from urlparse import urljoin


class TechcrunchSpider(scrapy.Spider):
    name = "techcrunch"
    allowed_domains = ["techcrunch.com"]
    start_urls = (
        'http://techcrunch.com',
        # 'http://techcrunch.com/page/4/',
        # 'http://techcrunch.com/2016/04/26/media-mogul-soledad-obrien-is-coming-to-disrupt-ny-2016/',
    )
    custom_settings = {
        'ITEM_PIPELINES': {
            'cv.pipelines.article.ArticlePipeline': 300
        }
    }

    # for everyday crawler use: 3 pages(60 articles) a day is enough to cover 36kr's update
    max_article_page = 3
    current_num = 0

    def parse(self, response):
        # parse homepage for update
        domain = 'http://techcrunch.com'
        if response.url == domain:
            lists = response.xpath('//a/@href').extract()
            lists = [x for x in lists if re.compile('http:\/\/techcrunch.com\/\d{4}\/\d{2}\/\d{2}.*').match(x)]
            lists = list(set(lists))
            for link in lists:
                yield scrapy.Request(link,callback=self.parse_page)
        # parse a specific page
        if re.compile('.*\/page\/\d+\/.*').match(response.url) is not None:
            lists = response.css('.post-title').xpath('.//a/@href').extract()
            for link in lists:
                yield scrapy.Request(link,callback=self.parse_page)
        # parse a single article
        if re.compile('.*\d{4}\/\d{2}\/\d{2}.*').match(response.url) is not None:
            item = self.parse_page(response)
            yield item

    def parse_page(self, response):
        domain = 'http://techcrunch.com'
        now_date = datetime.datetime.utcnow()
        now_date = now_date.strftime('%Y-%m-%d %H:%M:%S')

        item = ArticleItem()
        item['url'] = response.url
        item['title'] = response.css('.tweet-title::text').extract()
        # TODO filter out script and iframe ?
        item['content'] = ''.join(response.css('.article-entry').xpath('./*').extract())
        item['summary'] = ''
        item['published_ts'] = response.css('.title-left').xpath('.//time/@datetime').extract_first()
        item['created_ts'] = now_date
        item['updated_ts'] = now_date
        item['time_str'] = ''
        item['author_name'] = response.css('.byline').xpath('.//a/text()').extract_first()
        item['author_link'] = urljoin(domain, response.css('.byline').xpath('.//a/@href').extract_first())
        item['author_avatar'] = ''
        item['tags'] = ','.join(response.xpath('//meta[@name="category"]/@content').extract())
        item['site_unique_id'] = response.css('.social-share-list').xpath('@data-post-id').extract_first()
        item['author_id'] = 0
        item['author_email'] = ''
        item['author_phone'] = ''
        item['author_role'] = ''
        item['cover_real_url'] = ''
        item['source_type'] = ''
        item['views_count'] = ''
        item['cover'] = ''
        return item

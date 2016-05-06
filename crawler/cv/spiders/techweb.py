# -*- coding: utf-8 -*-
from datetime import datetime
from urlparse import urljoin

import re
import scrapy
from ..items.article import ArticleItem
from ..util.time import datetime_str_to_utc


class TechwebSpider(scrapy.Spider):
    name = "techweb"
    allowed_domains = ["techweb.com.cn"]
    start_urls = (
        # 'http://www.techweb.com.cn',
        'http://people.techweb.com.cn/list_1.shtml',
    )
    custom_settings = {
        'DOWNLOAD_DELAY': 0.15,
        'ITEM_PIPELINES': {
            'cv.pipelines.article.ArticlePipeline': 300
        }
    }

    max_article_page = 7650
    current_num = 675

    def parse(self, response):
        # parse homepage for update
        domain = 'http://www.techweb.com.cn'
        if response.url == domain:
            lists = self.parse_article_links(response)
            for link in lists:
                yield scrapy.Request(link, callback=self.parse_page)

        # parse multiple pages
        page = re.compile('^' + domain + '/page/(\d+)/').match(response.url)
        if page is not None:
            self.current_num = int(page.group(1))
            lists = self.parse_article_links(response)
            for link in lists:
                yield scrapy.Request(link, callback=self.parse_page)
            self.logger.info('[page] %s', response.url)
            # request next page
            if self.current_num < self.max_article_page:
                self.current_num += 1
                yield scrapy.Request(domain + '/page/' + str(self.current_num) + '/')

        # parse a specific page
        if re.compile('.*/list_(\d+)\.shtml').match(response.url) is not None:
            lists = self.parse_article_links(response)
            for link in lists:
                yield scrapy.Request(link, callback=self.parse_page)

        # parse a single article
        if re.compile('.*\d{4}/\d{2}/\d{2}.*').match(response.url) is not None:
            item = self.parse_page(response)
            yield item

    @staticmethod
    def parse_article_links(response):
        lists = response.xpath('//a/@href').extract()
        lists = [x for x in lists if re.compile('.*/\d{4}-\d{2}-\d{2}/\d+\.shtml').match(x)]
        lists = set(lists)
        return lists

    @staticmethod
    def parse_page(response):
        domain = 'http://www.techweb.com.cn'
        now_date = datetime.utcnow()
        now_date = now_date.strftime('%Y-%m-%d %H:%M:%S')
        published_ts = response.xpath('//meta[@name="timestamp"]/@content').extract_first()
        published_ts = datetime_str_to_utc(published_ts, 8)

        item = ArticleItem()
        return item
        item['url'] = response.url
        item['title'] = response.css('.tweet-title::text').extract()
        item['content'] = ''.join(response.css('.article-entry').xpath('./*').extract())
        item['summary'] = None
        item['published_ts'] = published_ts
        item['created_ts'] = now_date
        item['updated_ts'] = now_date
        item['time_str'] = None
        item['author_name'] = response.css('.byline').xpath('.//a/text()').extract_first()
        item['author_link'] = urljoin(domain, response.css('.byline').xpath('.//a/@href').extract_first())
        item['author_avatar'] = None
        item['tags'] = ','.join(response.xpath('//meta[@name="category"]/@content').extract())
        item['site_unique_id'] = response.css('.social-share-list').xpath('@data-post-id').extract_first()
        item['author_id'] = 0
        item['author_email'] = None
        item['author_phone'] = None
        item['author_role'] = None
        item['cover_real_url'] = None
        item['source_type'] = None
        item['views_count'] = 0
        item['cover'] = None
        return item

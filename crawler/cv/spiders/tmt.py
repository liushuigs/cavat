# -*- coding: utf-8 -*-

from datetime import datetime
from json import loads
from urlparse import urljoin

import re
from os.path import splitext, basename
from scrapy import Spider, Request
from ..items.article import ArticleItem
from ..util.time import datetime_str_to_utc


class TmtSpider(Spider):
    name = 'tmt'
    enabled_crontab = False
    limit = 10
    max_offset = 2000 * limit
    # max offset is nearly 13000 2016/05/04
    current_offset = 14000
    list_entry = 'http://www.tmtpost.com/api/lists/get_index_list?limit='+str(limit)+'&'
    start_urls = (
        'http://www.tmtpost.com',
        # list_entry + 'offset=' + str(current_offset),
    )
    custom_settings = {
        # 'DOWNLOAD_DELAY': 0.10,
        'DOWNLOAD_TIMEOUT': 6,
        'AUTOTHROTTLE_ENABLED': False,
        # 'AUTOTHROTTLE_DEBUG': True,
        'CONCURRENT_REQUESTS': 11, # equals article numbers in each page plus 1
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'ITEM_PIPELINES': {
            'cv.pipelines.article.ArticlePipeline': 300
        }
    }

    def parse(self, response):
        url = response.url
        home_articles = self.get_home_articles(response)
        if self.enabled_crontab:
            for link in home_articles:
                link = urljoin(url, link)
                yield Request(link, callback=self.parse_page)
        else:
            if "lists/get_index_list" in response.url:
                offset = int(response.url.find("offset=")) + 7
                self.current_offset = int(response.url[offset:])
                lists = self.parse_article_links(response)
                for link in lists:
                    yield Request(link, callback=self.parse_page)
                self.logger.info('[page] %s', response.url)
                # request next page
                if self.current_offset < self.max_offset:
                    self.current_offset += self.limit
                    yield Request(self.list_entry + 'offset=' + str(self.current_offset))

    def parse_article_links(self, response):
        try:
            ret = loads(response.body)
            return [x["short_url"] for x in ret["data"]]
        except ValueError as err:
            self.logger.warning('[json parse error] %s', response.url)
        return []

    @staticmethod
    def parse_page(response):
        domain = 'http://www.tmtpost.com'
        item = ArticleItem()

        article = response.css('.post-container article')
        if article is None:
            return item
        content = article.css('.inner').extract_first()
        if content is None:
            return item

        now_date = datetime.utcnow()
        now_date = now_date.strftime('%Y-%m-%d %H:%M:%S')

        item['url'] = response.url
        item['title'] = article.css('h1::text').extract_first()
        item['content'] = content
        item['summary'] = response.xpath('//meta[@name="description"]/@content').extract_first()
        item['published_ts'] = datetime_str_to_utc(article.css('.post-info .time::text').extract_first() + ':00', 8)
        item['created_ts'] = now_date
        item['updated_ts'] = now_date
        item['time_str'] = None
        item['author_name'] = article.css('.post-info').xpath('./a/@title').extract_first()
        item['author_link'] = urljoin(domain,
                                      article.css('.post-info').xpath('./a/@href').extract_first())
        item['author_avatar'] = response.css('.artilce-bar').xpath('.//img/@src').extract_first()
        item['tags'] = response.xpath('//meta[@name="keywords"]/@content').extract_first()
        item['site_unique_id'] = splitext(basename(response.url))[0]
        item['author_id'] = basename(article.css('.post-info').xpath('./a/@href').extract_first())
        item['author_email'] = None
        item['author_phone'] = None
        item['author_role'] = None
        item['cover_real_url'] = None
        item['source_type'] = None
        item['views_count'] = None
        item['cover'] = None
        return item

    @staticmethod
    def get_home_articles(response):
        all_links = re.findall(r'/\d+\.html', response.body)
        filtered_links = set(all_links)
        return filtered_links

# -*- coding: utf-8 -*-
import datetime
import json
import re
import scrapy
from cv.items.article import ArticleItem
from urlparse import urljoin
from ..util.time import datetime_str_to_utc
from twisted.python import log

# docs http://stackoverflow.com/questions/2493644/how-to-make-twisted-use-python-logging
observer = log.PythonLoggingObserver(loggerName=__name__)
observer.start()


class TechcrunchSpider(scrapy.Spider):
    name = "techcrunch"
    allowed_domains = ["techcrunch.com"]
    start_urls = (
        'http://techcrunch.com',
        # 'http://techcrunch.com/page/7/',
        # 'http://techcrunch.com/2016/04/26/media-mogul-soledad-obrien-is-coming-to-disrupt-ny-2016/',
    )
    custom_settings = {
        'DOWNLOAD_DELAY': 0.15,
        'ITEM_PIPELINES': {
            'cv.pipelines.article.ArticlePipeline': 300
        }
    }

    # for everyday crawler use: 3 pages(60 articles) a day is enough to cover 36kr's update
    max_article_page = 9
    current_num = 0

    def parse(self, response):
        # parse homepage for update
        domain = 'http://techcrunch.com'
        if response.url == domain:
            lists = self.parse_article_links(response)
            for link in lists:
                yield scrapy.Request(link, callback=self.parse_page)

        # parse multiple pages
        page = re.compile('^' + domain + '\/page\/(\d+)\/').match(response.url)
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
        # if re.compile('.*\/page\/\d+\/.*').match(response.url) is not None:
        #     lists = response.css('.post-title').xpath('.//a/@href').extract()
        #     for link in lists:
        #         yield scrapy.Request(link, callback=self.parse_page)

        # parse a single article
        if re.compile('.*\d{4}\/\d{2}\/\d{2}.*').match(response.url) is not None:
            item = self.parse_page(response)
            yield item

    @staticmethod
    def parse_article_links(response):
        lists = response.xpath('//a/@href').extract()
        lists = [x for x in lists if re.compile('http:\/\/techcrunch.com\/\d{4}\/\d{2}\/\d{2}.*').match(x)]
        lists = list(set(lists))
        return lists

    @staticmethod
    def parse_page(response):
        domain = 'http://techcrunch.com'
        now_date = datetime.datetime.utcnow()
        now_date = now_date.strftime('%Y-%m-%d %H:%M:%S')
        published_ts = response.xpath('//meta[@name="timestamp"]/@content').extract_first()
        published_ts = datetime_str_to_utc(published_ts, -7)

        item = ArticleItem()
        item['url'] = response.url
        item['title'] = response.css('.tweet-title::text').extract()
        # TODO filter out script and iframe ?
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

# -*- coding: utf-8 -*-
import datetime
import re
import scrapy
from ..items.article import ArticleItem
from ..util.time import datetime_str_to_utc
from os.path import basename, splitext
from twisted.python import log
from cv.models.article import Article

observer = log.PythonLoggingObserver(loggerName=__name__)
observer.start()


class IheimaSpider(scrapy.Spider):
    name = "iheima"
    allowed_domains = ["iheima.com"]
    # max page is 2481  2016/05/04
    max_article_page = 2481
    current_num = 912
    start_urls = (
        'http://www.iheima.com',
        # 'http://www.iheima.com/?page=' + str(current_num) + '&category=全部',
        # 'http://www.iheima.com/top/2016/0504/155585.shtml',
    )
    custom_settings = {
        'DOWNLOAD_DELAY': 0.15,
        'DOWNLOAD_TIMEOUT': 6,
        'AUTOTHROTTLE_ENABLED': True,
        # 'AUTOTHROTTLE_DEBUG': True,
        'CONCURRENT_REQUESTS': 11, # equals article numbers in each page plus 1
        'CONCURRENT_REQUESTS_PER_DOMAIN': 10,
        'DEFAULT_REQUEST_HEADERS': {
            'X-Requested-With': 'XMLHttpRequest'
        },
        'ITEM_PIPELINES': {
            'cv.pipelines.article.ArticlePipeline': 300
        }
    }

    def parse(self, response):
        # parse homepage for update
        domain = 'http://www.iheima.com'
        if response.url == domain:
            lists = self.parse_article_links(response)
            for link in lists:
                if Article.check_exists(link) is False:
                    yield scrapy.Request(link, callback=self.parse_page)

        # parse multiple pages
        page = re.compile('^' + domain + '/\?page=(\d*)&.*').match(response.url)
        if page is not None:
            self.current_num = int(page.group(1))
            lists = self.parse_article_links(response)
            for link in lists:
                yield scrapy.Request(link, callback=self.parse_page)
            self.logger.info('[page %d] %s', self.current_num, response.url)
            # request next page
            if self.current_num < self.max_article_page:
                self.current_num += 1
                yield scrapy.Request(domain + '/?page=' + str(self.current_num) + '&category=全部')

        # parse a single article
        if re.compile('.*\d*\.shtml').match(response.url) is not None:
            item = self.parse_page(response)
            yield item

    @staticmethod
    def parse_page(response):
        now_date = datetime.datetime.utcnow()
        now_date = now_date.strftime('%Y-%m-%d %H:%M:%S')
        published_ts = response.css('.author').xpath('.//time/text()').extract_first().strip() + ':00'
        published_ts = datetime_str_to_utc(published_ts, 8)

        item = ArticleItem()
        item['url'] = response.url
        item['title'] = response.css('.title::text').extract_first()
        item['content'] = ''.join(response.css('.main-content').css('p').extract())
        item['summary'] = response.xpath('//meta[@name="description"]/@content').extract_first()
        item['published_ts'] = published_ts
        item['created_ts'] = now_date
        item['updated_ts'] = now_date
        item['time_str'] = None
        item['author_name'] = response.css('.avatar').xpath('./img/@title').extract_first()
        item['author_link'] = None
        item['author_avatar'] = response.css('.avatar').xpath('./img/@src').extract_first()
        item['tags'] = ','.join(response.css('.tags .tag::text').extract())
        item['site_unique_id'] = splitext(basename(response.url))[0]
        item['author_id'] = 0
        item['author_email'] = None
        item['author_phone'] = None
        item['author_role'] = None
        item['cover_real_url'] = None
        item['source_type'] = None
        item['views_count'] = 0
        item['cover'] = response.css('.img-content').xpath('./img/@src').extract_first()
        return item

    @staticmethod
    def parse_article_links(response):
        lists = response.xpath('//a/@href').extract()
        lists = [x for x in lists if re.compile('http://www\.iheima\.com/.*\.shtml').match(x) and 'activity' not in x]
        lists = list(set(lists))
        return lists

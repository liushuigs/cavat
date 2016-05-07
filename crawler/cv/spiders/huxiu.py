# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from cv.items.article import ArticleItem
from datetime import datetime
from os.path import splitext, basename, dirname
from cv.util.time import datetime_str_to_utc
from urlparse import urlparse, urljoin
from twisted.python import log

# docs http://stackoverflow.com/questions/2493644/how-to-make-twisted-use-python-logging
observer = log.PythonLoggingObserver(loggerName=__name__)
observer.start()


class HuxiuSpider(Spider):
    name = "huxiu"
    allowed_domains = ["huxiu.com"]
    start_urls = (
        'http://www.huxiu.com',
    )
    custom_settings = {
        'ITEM_PIPELINES': {
            'cv.pipelines.article.ArticlePipeline': 300
        }
    }

    enabled_crontab = True

    def parse(self, response):
        url = urlparse(response.url)
        updated_everyday = self.get_latest_articles(response)
        if self.enabled_crontab:
            for link in updated_everyday:
                link = urljoin(response.url, link)
                yield Request(link, callback=self.parse_page)
        else:
            latest_link = max(updated_everyday)
            latest_link = urljoin(response.url, latest_link)
            latest_aid = basename(latest_link)
            int_aid = int(latest_aid)
            end_aid = 0
            while int_aid > end_aid:
                # TODO optimize unparsed url
                next_url = '/'.join([url.scheme+':/', url.netloc, 'article', str(int_aid)])
                int_aid -= 1
                yield Request(next_url, callback=self.parse_page)

    @staticmethod
    def parse_page(response):
        sel = response.selector
        domain = 'http://www.huxiu.com'
        item = ArticleItem()

        content = sel.css('#article_content').extract_first()
        if content is None:
            return item

        now_date = datetime.utcnow()
        now_date = now_date.strftime('%Y-%m-%d %H:%M:%S')

        item['url'] = response.url
        item['title'] = sel.xpath('//title/text()').extract_first()
        item['content'] = content
        item['summary'] = sel.xpath('//meta[@name="description"]/@content').extract_first()
        item['published_ts'] = datetime_str_to_utc(sel.css('.article-time::text').extract_first()+':00', 8)
        item['created_ts'] = now_date
        item['updated_ts'] = now_date
        item['time_str'] = None
        item['author_name'] = response.css('.box-author-info').css('.author-name a::text').extract_first()
        item['author_link'] = urljoin(domain,
                                      response.css('.box-author-info').css('.author-name a::attr(href)').extract_first())
        item['author_avatar'] = sel.css('.box-author-info').css('.author-face img::attr(src)').extract_first()
        item['tags'] = ','.join(sel.css('.tag-box').xpath(".//li[@class='transition']/text()").extract())
        item['site_unique_id'] = basename(response.url)
        if item['author_link'].find(urljoin(domain, '/member')) == 0:
            author_id = splitext(basename(item['author_link']))[0]
        else:
            author_id = 0
        item['author_id'] = author_id
        item['author_email'] = None
        item['author_phone'] = None
        item['author_role'] = sel.css('.box-author-info').css('.icon-team-auth::attr(title)').extract_first()
        item['cover_real_url'] = None
        item['source_type'] = None
        item['views_count'] = None
        item['cover'] = None
        return item

    @staticmethod
    def get_latest_articles(response):
        all_links = response.css('.wrap-left').xpath('.//a[contains(@href, "article")]/@href').extract()
        filtered_links = set([ dirname(link) for link in all_links if link.find('/article') == 0])
        return filtered_links

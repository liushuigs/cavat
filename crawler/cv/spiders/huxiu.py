# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from cv.items.article import ArticleItem
from datetime import datetime
from os.path import splitext, basename
from cv.util.time import datetime_str_to_utc
from urlparse import urlparse


class HuxiuSpider(Spider):
    name = "huxiu"
    allowed_domains = ["huxiu.com"]
    start_urls = (
        #'http://www.huxiu.com/',
        'http://www.huxiu.com/article/146942',
    )
    custom_settings = {
        'ITEM_PIPELINES': {
            'cv.pipelines.article.ArticlePipeline': 300
        }
    }

    def parse(self, response):
        aid = int(basename(response.url))
        url = urlparse(response.url)
        yield self.parse_page(response)
        while(aid > 0):
            # TODO optimize unparsed url
            next_url = '/'.join([url.scheme+':/', url.netloc, 'article', str(aid)])
            aid = aid-1
            yield Request(next_url, callback=self.parse_page)

    def parse_page(self, response):
        sel = response.selector
        item = ArticleItem()

        content = sel.css('#article_content').extract_first()
        if content == None:
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
        item['author_name'] = sel.css('.box-author-info').css('.author-name a::text').extract_first()
        item['author_link'] = sel.css('.box-author-info').css('.author-name a::attr(href)').extract_first()
        item['author_avatar'] = sel.css('.box-author-info').css('.author-face img::attr(src)').extract_first()
        item['tags'] = ','.join(sel.css('.tag-box').xpath(".//li[@class='transition']/text()").extract())
        item['site_unique_id'] = basename(response.url)
        item['author_id'] = splitext(basename(item['author_link']))[0]
        item['author_email'] = None
        item['author_phone'] = None
        item['author_role'] = sel.css('.box-author-info').css('.icon-team-auth::attr(title)').extract_first()
        item['cover_real_url'] = None
        item['source_type'] = None
        item['views_count'] = None
        item['cover'] = None
        return item

    def parse_updated_everyday(self, response):
        pass

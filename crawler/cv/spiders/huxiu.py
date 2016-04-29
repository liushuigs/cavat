# -*- coding: utf-8 -*-
import scrapy
from cv.items.article import ArticleItem
import datetime
from os.path import splitext, basename


class HuxiuSpider(scrapy.Spider):
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
        item = self.parse_page(response)
        yield item

    def parse_page(self, response):
        sel = response.selector
        item = ArticleItem()

        now_date = datetime.datetime.utcnow()
        now_date = now_date.strftime('%Y-%m-%d %H:%M:%S')

        item['url'] = response.url
        item['title'] = sel.xpath('//title/text()').extract_first()
        item['content'] = sel.css('#article_content').extract_first()
        item['summary'] = sel.xpath('//meta[@name="description"]/@content').extract_first()
        item['published_ts'] = self.datetime_str_to_utc(sel.css('.article-time::text').extract_first()+':00')
        item['created_ts'] = now_date
        item['updated_ts'] = now_date
        item['time_str'] = None
        item['author_name'] = sel.css('.box-author-info').css('.author-name a::text').extract_first()
        item['author_link'] = sel.css('.box-author-info').css('.author-name a::attr(href)').extract_first()
        item['author_avatar'] = sel.css('.box-author-info').css('.author-face img::attr(src)').extract_first()
        item['tags'] = ','.join(sel.css('.tag-box').xpath(".//li[@class='transition']/text()").extract())
        item['site_unique_id'] = sel.css('.pl-report').xpath('@aid').extract_first()
        item['author_id'] = splitext(basename(item['author_link']))[0]
        item['author_email'] = None
        item['author_phone'] = None
        item['author_role'] = sel.css('.box-author-info').css('.icon-team-auth::attr(title)').extract_first()
        item['cover_real_url'] = None
        item['source_type'] = None
        item['views_count'] = None
        item['cover'] = None
        return item

    @staticmethod
    def datetime_str_to_utc(date_str):
        timedelta = datetime.datetime.utcnow() - datetime.datetime.now()
        local_datetime = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        result_utc_datetime = local_datetime - timedelta
        return result_utc_datetime.strftime("%Y-%m-%d %H:%M:%S")

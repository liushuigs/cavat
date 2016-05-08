# -*- coding: utf-8 -*-
from datetime import datetime

import re
import scrapy
from ..items.article import ArticleItem
from ..util.time import datetime_str_to_utc


class TechwebSpider(scrapy.Spider):
    name = "techweb"
    allowed_domains = ["techweb.com.cn"]
    custom_settings = {
        'DOWNLOAD_DELAY': 0.15,
        # 'CONCURRENT_REQUESTS': 15,
        'ITEM_PIPELINES': {
            'cv.pipelines.article.ArticlePipeline': 300
        }
    }

    max_article_page = 100
    current_num = 1
    current_task = None

    def __init__(self, task=None, **kwargs):
        super(TechwebSpider, self).__init__(**kwargs)
        current_num = str(self.current_num)
        if task == 'home':
            url = ['http://www.techweb.com.cn']
        elif task == 'onepage':
            url = ['http://people.techweb.com.cn/list_'+current_num+'.shtml']
        elif task == 'pages':
            url = (
                # 'http://www.techweb.com.cn/news/list_' + current_num + '.shtml',
                'http://www.techweb.com.cn/smarthome/all/list_' + current_num + '.shtml',
                # 'http://www.techweb.com.cn/internet/all/list_' + current_num + '.shtml',
                # 'http://www.techweb.com.cn/it/all/list_' + current_num + '.shtml',
                # 'http://www.techweb.com.cn/tele/all/list_' + current_num + '.shtml',
                # 'http://www.techweb.com.cn/yuanchuang/all/list_' + current_num + '.shtml',
                # 'http://www.techweb.com.cn/data/all/list_' + current_num + '.shtml',
                # 'http://www.techweb.com.cn/mobile/all/list_' + current_num + '.shtml',
                # 'http://people.techweb.com.cn/list_' + current_num + '.shtml',
                # 'http://mi.techweb.com.cn/article/all/list_' + current_num + '.shtml',
                # 'http://mo.techweb.com.cn/article/all/list_' + current_num + '.shtml',
                # 'http://app.techweb.com.cn/list_' + current_num + '.shtml'
            )
        else:
            self.logger.error('Parameter Error!')
            return
        self.start_urls = url
        self.current_task = task

    def parse(self, response):
        task = self.current_task
        # parse homepage for update
        if task == 'home':
            lists = self.parse_homepage_links(response)
            cnt = 0
            for link in lists:
                yield scrapy.Request(link, callback=self.parse_item)
                cnt += 1
            self.logger.info('[parse homepage for update][total articles: %d]', cnt)

        # parse multiple pages of a specific domain
        if task == 'pages':
            lists = self.parse_article_links(response)
            for link in lists:
                yield scrapy.Request(link, callback=self.parse_item)
            page_num = int(re.compile(r'.*/list_(\d+)\.shtml.*').match(response.url).group(1))
            if self.current_num == page_num:
                self.max_article_page = self.get_page_total(response)
            self.logger.info('[current_num: %d, max_article_page: %d] [page] %s', page_num,
                             self.max_article_page, response.url)
            if self.current_num <= self.max_article_page:
                self.current_num += 1
                next_page_url = re.sub(r'_\d+', '_'+str(self.current_num), response.url)
                yield scrapy.Request(next_page_url)

        # parse pages based on first page in start_urls

        # parse a specific page
        if task == 'onepage':
            lists = self.parse_article_links(response)
            for link in lists:
                yield scrapy.Request(link, callback=self.parse_item)
            self.logger.info('[parse a specific page] %s', response.url)

    @staticmethod
    def parse_homepage_links(response):
        lists = response.xpath('//a/@href').extract()
        lists = [x for x in lists if re.compile('.*/\d{4}-\d{2}-\d{2}/\d+\.shtml').match(x)]
        lists = set(lists)
        return lists

    @staticmethod
    def get_page_total(response):
        lists = response.css('.page a::attr(href)').extract()
        id_lists = []
        for x in lists:
            m = re.compile(r'.*/list_(\d+)\.shtml.*').match(x)
            if m:
                id_lists.append(int(m.group(1)))
        return max(id_lists)

    @staticmethod
    def parse_article_links(response):
        lists = response.css('.con_list').xpath('.//a/@href').extract()
        lists = [x for x in lists if re.compile('.*/\d{4}-\d{2}-\d{2}/\d+\.shtml').match(x)]
        lists = set(lists)
        return lists

    @staticmethod
    def parse_item(response):
        now_date = datetime.utcnow()
        now_date = now_date.strftime('%Y-%m-%d %H:%M:%S')
        published_ts = response.css('#pubtime_baidu::text').extract_first()
        if published_ts:
            published_ts = published_ts.strip()
            published_ts = datetime.strptime(published_ts, '%Y.%m.%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            published_ts = datetime_str_to_utc(published_ts, 8)

        item = ArticleItem()
        item['url'] = response.url
        item['title'] = response.xpath('//meta[@property="og:title"]/@content').extract_first()
        item['content'] = ''.join(response.css('#artibody').xpath('./p').extract())
        item['summary'] = response.xpath('//meta[@name="description"]/@content').extract_first()
        item['published_ts'] = published_ts
        item['created_ts'] = now_date
        item['updated_ts'] = now_date
        item['time_str'] = None
        author_name = response.css('#author_baidu::text').extract_first()
        item['author_name'] = author_name.split(':')[1] if author_name else None
        item['author_link'] = None
        item['author_avatar'] = None
        item['tags'] = response.xpath('//meta[@name="keywords"]/@content').extract_first().rstrip(',')
        item['site_unique_id'] = response.xpath('//input[@name="newsid"]//@value').extract_first()
        item['author_id'] = 0
        item['author_email'] = None
        item['author_phone'] = None
        item['author_role'] = None
        item['cover_real_url'] = None
        item['source_type'] = response.css('#source_baidu a::text').extract_first().strip()
        item['views_count'] = 0
        item['cover'] = None
        return item

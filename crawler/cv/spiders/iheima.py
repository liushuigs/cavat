# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from ..items.article import ArticleItem
from datetime import datetime
from os.path import splitext, basename
import re

class TmtSpider(Spider):
    #name = 'iheima'
    start_urls = (
        'http://www.iheima.com',
    )
    custom_settings = {
        'ITEM_PIPELINES': {
            'cv.pipelines.article.ArticlePipeline': 300
        }
    }
    enabled_crontab = True

    def parse(self, response):
        url = response.url
        home_articles = self.get_home_articles(response)
        if self.enabled_crontab:
            pass
        else:
            gen_aid = (int(splitext(basename(link))[0]) for link in home_articles)
            start_aid = max(gen_aid)
            end_aid = 0
            # while(start_aid > end_aid):
            #     pass
        pass

    @staticmethod
    def parse_page(response):
        item = ArticleItem()

        content = response.css('#article_content').extract_first()
        if content is None:
            return item

        now_date = datetime.utcnow()
        now_date = now_date.strftime('%Y-%m-%d %H:%M:%S')

        item['url'] = response.url
        item['title'] = None
        item['content'] = content
        item['summary'] = None
        item['published_ts'] = None
        item['created_ts'] = now_date
        item['updated_ts'] = now_date
        item['time_str'] = None
        item['author_name'] = None
        item['author_link'] = None
        item['author_avatar'] = None
        item['tags'] = None
        item['site_unique_id'] = None
        item['author_id'] = None
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
        all_links = re.findall(r'\/\d+\.html', response.body)
        filtered_links = set(all_links)
        return filtered_links

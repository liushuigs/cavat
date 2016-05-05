# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from ..items.article import ArticleItem
from datetime import datetime
import re
from ..util.time import datetime_str_to_utc
from os.path import splitext, basename


class PedailySpider(Spider):
    name = 'pedaily'
    current_page = 2442
    total_page = 6745
    start_urls = (
        # 'http://www.pedaily.cn',
        'http://www.pedaily.cn/top/handlers/Handler.ashx?action=newslist-all&p=' + str(current_page) +
        '&url=http://www.pedaily.cn/top/newslist.aspx?c=all',
    )
    custom_settings = {
        'ITEM_PIPELINES': {
            'cv.pipelines.article.ArticlePipeline': 300
        }
    }

    def parse(self, response):
        url = response.url
        articles = get_list_of_curpage(response)
        if url == 'http://www.pedaily.cn':
            for link in articles:
                yield Request(link, callback=parse_page)
        else:
            for link in articles:
                yield Request(link, callback=parse_page)
                last_page = self.total_page
            if self.current_page <= last_page:
                self.current_page += 1
                cur_url = 'http://www.pedaily.cn/top/handlers/Handler.ashx?action=newslist-all&p=' + \
                        str(self.current_page)+'&url=http://www.pedaily.cn/top/newslist.aspx?c=all'
                self.logger.info('[page %d] %s', self.current_page, cur_url)
                yield Request(cur_url)

def get_list_of_curpage(response):
    list_submain = ['news', 'pe', 'newseed', 'if']
    set_link = set()
    for sub in list_submain:
        set_link = set_link | set(re.findall(r'http://'+sub+'\.pedaily\.cn/\d+/\d+\.shtml', response.body))
    return set_link


def parse_page(response):
    item = ArticleItem()

    content = response.css('#news-content').extract_first()
    if content is None:
        return item

    now_date = datetime.utcnow()
    now_date = now_date.strftime('%Y-%m-%d %H:%M:%S')

    item['url'] = response.url
    item['title'] = response.xpath('//h1/text()').extract_first()
    item['content'] = content
    item['summary'] = response.css('.subject').xpath('./text()').extract_first()
    item['published_ts'] = datetime_str_to_utc(response.css('.info .date::text').extract_first() + ':00', 8)
    item['created_ts'] = now_date
    item['updated_ts'] = now_date
    item['time_str'] = None
    author_name = response.css('.info ').xpath('./div[1]').xpath('./text()').extract_first().strip()
    if not author_name:
        author_name = response.css('.info ').xpath('./div[2]').xpath('./text()').extract_first().strip()
    item['author_name'] = ' '.join(author_name.split())
    item['author_link'] = None
    item['author_avatar'] = None
    item['tags'] = response.xpath('//meta[@name="keywords"]/@content').extract_first()
    item['site_unique_id'] = splitext(basename(response.url))[0]
    item['author_id'] = None
    item['author_email'] = None
    item['author_phone'] = None
    item['author_role'] = None
    item['cover_real_url'] = None
    item['source_type'] = None
    item['views_count'] = None
    item['cover'] = None
    return item

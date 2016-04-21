# -*- coding: utf-8 -*-
import datetime
import json
import re
import scrapy
from cv.items.article import ArticleItem
from urlparse import urljoin


class A36krSpider(scrapy.Spider):
    name = "36kr"
    allowed_domains = ["36kr.com"]
    list_entry = 'http://36kr.com/asynces/posts/info_flow_post_more.json?b_url_code='
    start_urls = (
        'http://36kr.com',
        # list_entry + '5046211',
    )
    custom_settings = {
        'ITEM_PIPELINES': {
            'cv.pipelines.a36kr.ArticlePipeline': 300
        }
    }

    # for everyday crawler use: 3 pages(60 articles) a day is enough to cover 36kr's update
    max_article_page = 3
    current_num = 0

    def parse(self, response):
        print response.url
        domain = 'http://36kr.com'

        # from homepage parse the first list entry
        if response.url == domain:
            first_article_code = re.search('url_code&quot;:(\d+),&quot;views_count', response.body).group(1)
            print 'first_article_code' + first_article_code
            yield scrapy.Request(self.list_entry + first_article_code)

        # from the list entry parse articles
        if 'b_url_code' in response.url:
            lists = json.loads(response.body_as_unicode())
            for i, page in enumerate(lists['data']['feed_posts']):
                yield scrapy.Request(domain + '/p/' + str(page['url_code']) + '.html',
                                     meta={'data': page},
                                     callback=self.parse_page)
                if (i+1) == len(lists['data']['feed_posts']):
                    print 'end of list'.center(100, '-')
                    self.current_num += 1
                    if self.current_num + 1 < self.max_article_page:
                        yield scrapy.Request(self.list_entry + str(page['url_code']))

    def parse_page(self, response):
        domain = 'http://36kr.com'
        data = response.meta['data']
        obj = response.css('.js-react-on-rails-component') \
            .xpath('@data-props').extract()
        result = json.loads(obj[0])
        post = result['data']['post']

        now_date = datetime.datetime.utcnow()
        now_date = now_date.strftime('%Y-%m-%d %H:%M:%S')

        item = ArticleItem()
        item['url'] = urljoin(domain, result['data']['router'])
        item['title'] = post['title']
        item['content'] = post['display_content']
        item['summary'] = post['summary']
        item['published_ts'] = self.datetime_str_to_utc(post['published_at'])
        item['created_ts'] = now_date
        item['updated_ts'] = now_date
        item['time_str'] = ''
        item['author_name'] = post['author']['display_name']
        item['author_link'] = urljoin(domain, post['author']['domain_path'])
        item['author_avatar'] = post['author']['avatar']
        item['tags'] = ','.join(post['display_tag_list'])
        item['site_unique_id'] = data['url_code']
        item['author_id'] = data['author']['id']
        item['author_email'] = data['author'].get('email', "")
        item['author_phone'] = data['author'].get('phone', "")
        item['author_role'] = data['author'].get('role', "")
        item['cover_real_url'] = data['cover_real_url']
        item['source_type'] = data['source_type']
        item['views_count'] = data['views_count']
        item['cover'] = data['cover']
        yield item

    @staticmethod
    def datetime_str_to_utc(date_str):
        dt = datetime.datetime.strptime(date_str[:19], "%Y-%m-%dT%H:%M:%S")
        ds = dt - datetime.timedelta(hours=8)
        return ds.strftime('%Y-%m-%d %H:%M:%S')

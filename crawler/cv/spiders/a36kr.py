# -*- coding: utf-8 -*-
import datetime
import json
import scrapy
from cv.items.article import ArticleItem
from urlparse import urljoin


class A36krSpider(scrapy.Spider):
    name = "36kr"
    allowed_domains = ["36kr.com"]
    start_urls = (
        'http://36kr.com/asynces/posts/info_flow_post_more.json?b_url_code=5046096',
    )
    custom_settings = {
        'ITEM_PIPELINES': {
            'cv.pipelines.a36kr.ArticlePipeline': 300
        }
    }

    def parse(self, response):
        # filename = 'data/'+response.url.split("/")[-1]
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # print response.body
        domain = 'http://36kr.com'
        if 'b_url_code' in response.url:
            lists = json.loads(response.body_as_unicode())
            for page in lists['data']['feed_posts']:
                yield scrapy.Request(domain + '/p/' + str(page['url_code']) + '.html',
                                     meta={'data': page},
                                     callback=self.parse_page)

    def request_next_page(self):
        pass

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

import datetime
import scrapy
from scrapy.selector import Selector
from cv.items.article import ArticleItem
from twisted.python import log

# docs http://stackoverflow.com/questions/2493644/how-to-make-twisted-use-python-logging
observer = log.PythonLoggingObserver(loggerName=__name__)
observer.start()


class WeixinSpider(scrapy.Spider):
    """
    usage:
    get list from this place:
    http://mp.weixin.qq.com/profile?src=3&timestamp=1463987171&ver=1&signature=dBR2A9gcrFso5*ujyX*ZUo3pRCKAzIqPqNPtj
    WW2yf7INhCd7hQL4i91RIccmkURt7QrELuxBYw6qC7sxM3eHQ==
    """
    name = "weixin"
    allowed_domains = ["weixin.qq.com"]
    start_urls = (
        'http://mp.weixin.qq.com/s?timestamp=1463977412&src=3&ver=1&signature=2nZDsMN6T63t4kAuwSHoyBpCKFRu0IGwppuYYgYEL'
        'uTz9PLwotYoFZMMe-waZib9wiQLZ1n-l1NHBXJNMMJLl9cSumnOuMekg9sWVnAau6chaLNrhvr9oJFfKfG5VCJgT08QH9FMehgaq*D22SHFoT'
        'Gq-D0w7*8YWTMzcydKj4E=',
    )
    custom_settings = {
        'ITEM_PIPELINES': {
            'cv.pipelines.article.ArticlePipeline': 300
        }
    }

    def __init__(self, url=None, **kwargs):
        super(WeixinSpider, self).__init__(**kwargs)
        if kwargs.get('file') is not None:
            file_name = kwargs.get('file')
            file_obj = open(file_name, 'r')
            text = file_obj.read()
            self.start_urls = self.parse_links(text)
        elif url is not None:
            self.start_urls = [url]
        else:
            self.start_urls = []

    def parse(self, response):
        item = self.parse_page(response)
        yield item

    @staticmethod
    def parse_links(text):
        response = Selector(text=text)
        links = response.css('.weui_media_title').xpath('//@hrefs').extract()
        links = list(set(links))
        links = [u'http://mp.weixin.qq.com'+item for item in links]
        return links

    @staticmethod
    def parse_page(response):
        now_date = datetime.datetime.utcnow()
        now_date = now_date.strftime('%Y-%m-%d %H:%M:%S')
        published_ts = response.css('#post-date::text').extract_first() + ' 00:00:00'

        item = ArticleItem()
        item['url'] = response.url
        item['title'] = response.xpath('//title/text()').extract_first()
        item['content'] = ''.join(response.css('.rich_media_content').xpath('./*').extract())
        item['summary'] = None
        item['published_ts'] = published_ts
        item['created_ts'] = now_date
        item['updated_ts'] = now_date
        item['time_str'] = None
        item['author_name'] = response.css('.profile_nickname::text').extract_first()
        item['author_link'] = response.css('.profile_meta_value::text').extract_first()
        item['author_avatar'] = None
        item['tags'] = None
        item['site_unique_id'] = None
        item['author_id'] = 0
        item['author_email'] = None
        item['author_phone'] = None
        item['author_role'] = None
        item['cover_real_url'] = None
        item['source_type'] = None
        item['views_count'] = 0
        item['cover'] = None
        return item

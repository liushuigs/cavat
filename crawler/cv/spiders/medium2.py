import scrapy
from cv.items.raw_data import RawDataItem
from cv.models.raw_data import RawData
from cv.pipelines.medium import black_list
import re


class Medium2Spider(scrapy.Spider):
    name = "medium2"
    allowed_domains = ["medium.com"]
    handle_httpstatus_list = [404, 301]
    depth = 1
    start_urls = (
        'https://medium.com',
        'https://medium.com/browse/b99480981476',
    )
    custom_settings = {
        # 'DOWNLOAD_DELAY': 0.80,
        # 'DOWNLOAD_TIMEOUT': 1,
        # 'AUTOTHROTTLE_ENABLED': True,
        # 'CONCURRENT_REQUESTS': 16,
        # 'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'ITEM_PIPELINES': {
            'cv.pipelines.raw_data.RawDataPipeline': 300
        },
    }

    def __init__(self, depth=None, url=None, **kwargs):
        super(Medium2Spider, self).__init__(**kwargs)
        if url is not None:
            self.start_urls = [url]
        elif depth is not None:
            self.depth = int(depth)
            start_urls = [x["url"] for x in RawData.get_by_depth(self.depth)]
            valid_urls = [url for url in start_urls if self.is_valid_url(url)]
            # invalid_urls = [url for url in start_urls if self.is_valid_url(url) is False]
            # self.mark_as_parsed(invalid_urls)
            self.start_urls = valid_urls

    @staticmethod
    def mark_as_parsed(urls):
        for url in urls:
            RawData.mark_as_parsed(url)

    @staticmethod
    def is_valid_url(url):
        flag = True
        for rule in black_list:
            if re.match(rule, url):
                flag = False
        return flag

    def make_requests_from_url(self, url):
        return scrapy.Request(url, dont_filter=True, meta={
            'dont_redirect': True,
            'handle_httpstatus_list': [301, 404, 302, 410]
        })

    def parse(self, response):
        entry = RawDataItem()
        entry["url"] = response.url
        entry["http_status"] = str(response.status)
        entry["depth"] = self.depth
        entry["parsed_as_entry"] = 1
        entry["domain"] = 'medium.com'
        if entry["http_status"] == '200':
            entry["html"] = response.body
        else:
            entry["html"] = ""
        self.logger.info('[create entry] %s', response.url)
        yield entry

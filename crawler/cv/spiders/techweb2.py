import scrapy
from cv.items.raw_data import RawDataItem
from cv.models.raw_data import RawData


class Techweb2Spider(scrapy.Spider):
    name = "techweb2"
    allowed_domains = ["techweb.com.cn"]
    depth = 1
    start_urls = (
        'http://www.techweb.com.cn',
        'http://www.techweb.com.cn/internet/2016-05-10/2329779.shtml',
    )
    custom_settings = {
        'DOWNLOAD_DELAY': 0.80,
        'DOWNLOAD_TIMEOUT': 6,
        'AUTOTHROTTLE_ENABLED': True,
        'CONCURRENT_REQUESTS': 16,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'ITEM_PIPELINES': {
            'cv.pipelines.raw_data.RawDataPipeline': 300
        }
    }

    def __init__(self, depth=None, url=None, **kwargs):
        super(Techweb2Spider, self).__init__(**kwargs)
        if url is not None:
            self.start_urls = [url]
        elif depth is not None:
            self.depth = int(depth)
            self.start_urls = [x["url"] for x in RawData.get_by_depth(self.depth)]
            print self.start_urls

    def make_requests_from_url(self, url):
        return scrapy.Request(url, dont_filter=True, meta={
            'dont_redirect': True,
            'handle_httpstatus_list': [301, 302]
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
        self.logger.info('[create entry] %s', response.url)
        yield entry

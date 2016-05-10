import scrapy


class RawDataItem(scrapy.Item):
    url = scrapy.Field()
    domain = scrapy.Field()
    created_ts = scrapy.Field()
    updated_ts = scrapy.Field()
    depth = scrapy.Field()
    http_status = scrapy.Field()
    html = scrapy.Field()
    parsed_as_entry = scrapy.Field()

import scrapy


class ArticleItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    summary = scrapy.Field()
    published_ts = scrapy.Field()
    created_ts = scrapy.Field()
    updated_ts = scrapy.Field()
    time_str = scrapy.Field()
    author_name = scrapy.Field()
    author_link = scrapy.Field()
    author_avatar = scrapy.Field()
    tags = scrapy.Field()

import datetime
import re
import scrapy
from cv.items.article import ArticleItem
from ..util.time import datetime_str_to_utc
from cv.models.article import Article


class VenturebeatSpider(scrapy.Spider):
    name = "venturebeat"
    allowed_domains = ["venturebeat.com"]
    # max pages 1430 2016/05/09
    max_article_page = 100
    current_num = 12
    start_urls = (
        'http://venturebeat.com',
        # 'http://venturebeat.com/page/' + str(current_num) + '/',
        # 'http://venturebeat.com/2015/07/21/jet-wants-to-woo-you-away-from-amazon-by-being-your-best-shopping-buddy/',
    )
    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
        'DOWNLOAD_DELAY': 0.50,
        'DOWNLOAD_TIMEOUT': 20,
        'AUTOTHROTTLE_ENABLED': True,
        'COOKIES_ENABLED': False,
        # 'REDIRECT_ENABLED': False,
        # 'AUTOTHROTTLE_DEBUG': True,
        'CONCURRENT_REQUESTS': 16,  # equals article numbers in each page plus 1
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'ITEM_PIPELINES': {
            'cv.pipelines.article.ArticlePipeline': 300
        },
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'en'
        },
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
    }

    def make_requests_from_url(self, url):
        return scrapy.Request(url, dont_filter=True, meta={
            'dont_redirect': True,
            'handle_httpstatus_list': [301, 302]
        })

    def parse(self, response):
        # parse homepage for update
        domain = 'http://venturebeat.com'
        if response.url == domain:
            lists = self.parse_article_links(response)
            for link in lists:
                if Article.check_exists(link) is False:
                    yield scrapy.Request(link, callback=self.parse_page)

        # parse multiple pages
        page = re.compile('^' + domain + '\/page\/(\d+)\/').match(response.url)
        if page is not None:
            self.current_num = int(page.group(1))
            lists = self.parse_article_links(response)
            for link in lists:
                yield scrapy.Request(link, callback=self.parse_page)
            self.logger.info('[page] %s', response.url)
            # request next page
            if self.current_num < self.max_article_page:
                self.current_num += 1
                yield scrapy.Request(domain + '/page/' + str(self.current_num) + '/')

        # parse a single article
        if re.compile('.*\d{4}\/\d{2}\/\d{2}.*').match(response.url) is not None:
            item = self.parse_page(response)
            yield item

    @staticmethod
    def parse_article_links(response):
        lists = response.css('.article-title a').xpath('@href').extract()
        lists = [x for x in lists if re.compile('http:\/\/venturebeat.com\/\d{4}\/\d{2}\/\d{2}.*').match(x)]
        lists = list(set(lists))
        return lists

    @staticmethod
    def parse_page(response):
        domain = 'http://venturebeat.com'
        now_date = datetime.datetime.utcnow()
        now_date = now_date.strftime('%Y-%m-%d %H:%M:%S')
        published_ts = response.xpath('//meta[@property="bt:pubDate"]/@content').extract_first()
        time_str = published_ts[:19].replace('T', ' ')
        timezone = int(published_ts[19:22])
        published_ts = datetime_str_to_utc(time_str, timezone)
        short_url = response.xpath('//link[@rel="shortlink"]/@href').extract_first()

        item = ArticleItem()
        item['url'] = response.url
        item['title'] = response.css('h1.article-title::text').extract_first()
        item['content'] = ''.join(response.css('.article-content').xpath('./*').extract())
        item['summary'] = None
        item['published_ts'] = published_ts
        item['created_ts'] = now_date
        item['updated_ts'] = now_date
        item['time_str'] = None
        item['author_name'] = response.xpath('//meta[@property="bt:author"]/@content').extract_first()
        item['author_link'] = response.css('.article-byline a.author').xpath('@href').extract_first()
        item['author_avatar'] = None
        item['tags'] = ','.join(response.css('.article-tags a::text').extract())
        item['site_unique_id'] = short_url[13:]
        item['author_id'] = 0
        item['author_email'] = None
        item['author_phone'] = None
        item['author_role'] = None
        item['cover_real_url'] = None
        item['source_type'] = None
        item['views_count'] = 0
        item['cover'] = response.css('.article-media-header img').xpath('@src').extract_first()
        return item

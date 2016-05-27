import datetime
import re
import scrapy
from cv.items.article import ArticleItem
from ..util.time import datetime_str_to_utc
from twisted.python import log
from cv.models.article import Article

# docs http://stackoverflow.com/questions/2493644/how-to-make-twisted-use-python-logging
observer = log.PythonLoggingObserver(loggerName=__name__)
observer.start()


class TheNextWebSpider(scrapy.Spider):
    name = "thenextweb"
    allowed_domains = ["thenextweb.com"]
    list_entry = 'http://thenextweb.com/wp-content/themes/cyberdelia/ajax/partials/grid-pager.php?slug=&taxo=&'
    start_urls = (
        'http://thenextweb.com',
        # list_entry + 'page=5651',
        # 'http://thenextweb.com/us/2016/05/01/tor-vpn-users-will-target-hacks-new-us-spying-rules/',
    )
    custom_settings = {
        'DOWNLOAD_DELAY': 0.80,
        'DOWNLOAD_TIMEOUT': 6,
        'AUTOTHROTTLE_ENABLED': True,
        # 'AUTOTHROTTLE_DEBUG': True,
        'CONCURRENT_REQUESTS': 13, # equals article numbers in each page plus 1
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'ITEM_PIPELINES': {
            'cv.pipelines.article.ArticlePipeline': 300
        }
    }

    # for everyday crawler use: 3 pages(60 articles) a day is enough to cover 36kr's update
    # max page: 6270 2016/05/03
    max_article_page = 6270
    current_num = 431
    enable_multi_page = True

    def parse(self, response):
        # parse homepage for update
        domain = 'http://thenextweb.com'
        if response.url == domain:
            lists = self.parse_article_homepage(response)
            for link in lists:
                if Article.check_exists(link) is False:
                    yield scrapy.Request(link, callback=self.parse_page)

        # parse multiple pages
        if self.enable_multi_page:
            page = re.compile('.*page=(\d+)').match(response.url)
            if page is not None:
                self.current_num = int(page.group(1))
                lists = self.parse_article_links(response)
                for link in lists:
                    yield scrapy.Request(link, callback=self.parse_page)
                self.logger.info('[page] %s', response.url)
                # request next page
                if self.current_num < self.max_article_page:
                    self.current_num += 1
                    yield scrapy.Request(self.list_entry + 'page=' + str(self.current_num))
        # parse a specific page
        else:
            if re.compile('^' + domain + '/latest/page/(\d+)/').match(response.url) is not None:
                lists = self.parse_article_links(response)
                for link in lists:
                    yield scrapy.Request(link, callback=self.parse_page)

        # parse a single article
        if re.compile('.*\d{4}\/\d{2}\/\d{2}.*').match(response.url) is not None:
            item = self.parse_page(response)
            yield item

    @staticmethod
    def parse_article_homepage(response):
        lists = response.xpath('//a/@href').extract()
        lists = [x for x in lists if re.compile('.*\d{4}\/\d{2}\/\d{2}.*').match(x)]
        lists = list(set(lists))
        return lists

    @staticmethod
    def parse_article_links(response):
        lists = response.css('.story-title>a').xpath('@href').extract()
        return lists

    @staticmethod
    def parse_page(response):
        now_date = datetime.datetime.utcnow()
        now_date = now_date.strftime('%Y-%m-%d %H:%M:%S')
        published_ts = response.xpath('//meta[@property="article:published_time"]/@content').extract_first()
        time_str = published_ts[:19].replace('T', ' ')
        timezone = int(published_ts[19:22])
        published_ts = datetime_str_to_utc(time_str, timezone)
        email = response.css('.post-author-contact').xpath('@href').extract_first()
        email = email[7:] if 'mailto' in email else None

        item = ArticleItem()
        item['url'] = response.url
        item['title'] = response.xpath('//title/text()').extract_first()
        item['content'] = ''.join(response.css('.post-body').xpath('./*').extract())
        item['summary'] = response.xpath('//meta[@property="og:description"]/@content').extract_first()
        item['published_ts'] = published_ts
        item['created_ts'] = now_date
        item['updated_ts'] = now_date
        item['time_str'] = None
        item['author_name'] = response.xpath('//meta[@name="author"]/@content').extract_first()
        item['author_link'] = response.xpath('//meta[@property="article:author"]/@content').extract_first()
        item['author_avatar'] = None
        item['tags'] = None
        item['site_unique_id'] = response.xpath('//link[@rel="shortlink"]/@href').extract_first()[25:]
        item['author_id'] = 0
        item['author_email'] = email
        item['author_phone'] = None
        item['author_role'] = None
        item['cover_real_url'] = None
        item['source_type'] = None
        item['views_count'] = 0
        item['cover'] = response.css('.post-featuredImage img').xpath('@data-src').extract_first()
        return item

"""
usage: add following to crontab
1 * * * * cd $PROJECT_DIRECTOR/crawler/ && ./env/bin/python scripts/crontab.py >>log.log 2>&1
"""
import os
import sys
# add crawler directory to search path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# add mac osx system site-packages to the search path
sys.path.append('/Library/Python/2.7/site-packages')
from scrapy.crawler import CrawlerProcess
from cv.spiders.a36kr import A36krSpider
from cv.spiders.techcrunch import TechcrunchSpider
from cv.spiders.thenextweb import TheNextWebSpider
from cv.spiders.huxiu import HuxiuSpider
from cv.spiders.tmt import TmtSpider
from cv.spiders.iheima import IheimaSpider
from cv.spiders.pedaily import PedailySpider
from cv.spiders.medium import MediumSpider
from scripts.update_domain import update_table

process = CrawlerProcess()
process.crawl(A36krSpider)
process.crawl(TechcrunchSpider)
process.crawl(TheNextWebSpider)
process.crawl(HuxiuSpider)
process.crawl(TmtSpider)
process.crawl(IheimaSpider)
process.crawl(PedailySpider)
process.crawl(MediumSpider)
process.start()

update_table()

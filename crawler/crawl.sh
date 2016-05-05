#!/bin/bash

# add this file to crontab
. env/bin/activate
scrapy crawl 36kr >> crawl.log
scrapy crawl techcrunch >> crawl.log
scrapy crawl thenextweb >> crawl.log
scrapy crawl huxiu >> crawl.log
scrapy crawl tmt >> crawl.log
scrapy crawl iheima >> crawl.log
scrapy crawl pedaily >> crawl.log
scrapy crawl startup-partner >> crawl.log

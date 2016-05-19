#!/bin/bash

# add this file to crontab
cd /Users/xfs/workspace/cavat
. env/bin/activate
cd crawler
scrapy crawl 36kr
scrapy crawl techcrunch
scrapy crawl thenextweb
scrapy crawl huxiu
scrapy crawl tmt
scrapy crawl iheima
scrapy crawl pedaily
scrapy crawl startup-partner
scrapy crawl medium
python scripts/update_domain.py

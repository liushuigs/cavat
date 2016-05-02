#!/bin/bash

# add this file to crontab
. env/bin/activate
scrapy crawl 36kr >> crawl.log
scrapy crawl techcrunch >> crawl.log
scrapy crawl huxiu >> crawl.log

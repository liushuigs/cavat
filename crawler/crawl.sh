#!/bin/bash

# add this file to crontab
. env/bin/activate
scrapy crawl 36kr >> crawl.log
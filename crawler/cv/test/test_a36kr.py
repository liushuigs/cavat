import os
from os.path import dirname
from scrapy.selector import Selector
from scrapy.http import HtmlResponse


def parse_from_file():
    filename = os.path.abspath(__file__)
    with open(dirname(dirname(filename)) + '/data/5045706.html', 'r') as f:
        target = Selector(text=f.read())

    obj = target.css('.js-react-on-rails-component').xpath('@data-props').extract()
    result = obj[0]
    print result


def parse_body():
    pass


def parse_from_url():
    # TODO http://doc.scrapy.org/en/master/topics/selectors.html#topics-selectors
    pass


if __name__ == '__main__':
    parse_from_file()
    # parse_from_url()

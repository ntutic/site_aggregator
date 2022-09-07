# Quotes with Playwright example

import scrapy
from flights.items import QuotesItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    custom_settings = {
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        #"PLAYWRIGHT_LAUNCH_OPTIONS": {
        #    "proxy": {
        #        "server": "http://myproxy.com:3128",
        #        "username": "user",
        #        "password": "pass",
        #    },
        #}
    }

    def start_requests(self):
        url = "https://quotes.toscrape.com/js/"
        yield scrapy.Request(url, meta={'playwright': True})

    def parse(self, response):
        quote_item = QuotesItem()
        for quote in response.css('div.quote'):
            quote_item['text'] = quote.css('span.text::text').get()
            quote_item['author'] = quote.css('small.author::text').get()
            quote_item['tags'] = quote.css('div.tags a.tag::text').getall()
            yield quote_item
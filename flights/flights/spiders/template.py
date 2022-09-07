# Empty template for playwright spider

import scrapy
from flights.items import FlightItem
from scrapy_playwright.page import PageMethod

class TemplateSpider(scrapy.Spider):
    name = ''
    custom_settings = {
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }

    def start_requests(self):
        url = ""
        yield scrapy.Request(url, meta=dict(
            playwright = True,
            playwright_include_page = True, 
            playwright_page_methods = [
                PageMethod("screenshot", path=f"flights/data/recent_startrequests_{self.name}.png", full_page=True),
            ],
            errback=self.errback,
        ))

    def preload(self, response):
        return response

    async def parse(self, response):
        response = self.preload(response)

        _item = scrapy.Item()
        self.logger.info(response.url)

        for element in response.css(''):
            yield _item


    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
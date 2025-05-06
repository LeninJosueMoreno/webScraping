import scrapy
from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.selector import Selector

from itemloaders.processors import MapCompose


class Hotel(Item):
    nombre = Field()
    score = Field()
    descripcion = Field()
    amenities = Field()


class TripAdvisor(CrawlSpider):
    name = "Hoteles"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    allowed_domains = ['tripadvisor.com']
    start_urls = ['https://www.tripadvisor.com/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']
    download_delay = 2
    rules = (
        Rule(LinkExtractor(
            allow=r'/Hotel_Review-'
        ), follow=True, callback="parse_item"),
    )

    def quitarSignoDolar(self, texto):
        return texto.replace("$", "")

    def parse_item(self, response):
        sel = Selector(response)

        item = ItemLoader(Hotel(), sel)
        item.add_xpath('nombre', '//h1[@id="HEADING"]/text()')
        item.add_xpath('score', '//span[@class="KJyXc P"]/text()', MapCompose(self.quitarSignoDolar()))
        item.add_xpath('descripcion', '//div[@id="ABOUT_TAB"]//div[@class="fIrGe _T"]//text()',
                       MapCompose(lambda i: i.replace('\n', '').replace('\r', '')))
        item.add_xpath('amenities', '//div[contains(@data-test-target, "amenity_text")]/text()')

        yield item.load_item() 
 
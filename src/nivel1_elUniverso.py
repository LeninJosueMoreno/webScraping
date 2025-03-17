from platform import processor

from jmespath.ast import field
from scrapy.crawler import CrawlerProcess
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup

class Noticia(Item):

    id = Field()
    titular = Field()
    descripcion = Field()


class ElUniversoSpider(Spider):
    name = "MiSegundoSpider"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

    start_urls = ["https://www.eluniverso.com/deportes/"]

    def parse(self, response):
       sel = Selector(response)
       noticias = sel.xpath('//div[contains(@class, "content-feed")]/ul/li')
       for i, elem in enumerate (noticias):
           item = ItemLoader(Noticia(), elem)

           item.add_xpath('titular', './/h2/a/text()')
           item.add_xpath('descripcion', './/p/text()')
           item.add_value('id', i)
           yield item.load_item()

# Corriendo Scrapy sin la terminal
process = CrawlerProcess({
    'FEED_FORMAT': 'csv',
    'FEDD_URI': 'Resultados.csv'
})
process.crawl(ElUniversoSpider)
process.start()
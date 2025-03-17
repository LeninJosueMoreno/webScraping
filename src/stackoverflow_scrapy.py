from bs4 import BeautifulSoup
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

from src.nivel1_elUniverso import Noticia


class Pregunta(Item):
    id = Field()
    pregunta = Field()
    descripcion = Field()

class StackOverflowSpider(Spider):
    name = "MiPrimerSpider"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    start_urls = ['https://stackoverflow.com/questions']

    def parse(self, response):
        sel = Selector(response)
        titulo_de_pagina = sel.xpath('//h1/text()').get()
        print(titulo_de_pagina)
        preguntas = sel.xpath('//div[@id="questions"]//div[contains(@class,"s-post-summary ")]')
        i = 0
        for pregunta in preguntas:
            item = ItemLoader(Pregunta(), pregunta)  # Instancio mi ITEM con el selector en donde estan los datos para llenarlo

            # Lleno las propiedades de mi ITEM a traves de expresiones XPATH a buscar dentro del selector "pregunta"
            item.add_xpath('pregunta', './/h3/a/text()')
            item.add_xpath('descripcion', './/div[@class="s-post-summary--content-excerpt"]/text()')
            item.add_value('id', i)
            i += 1
            yield item.load_item()  # Hago Yield de la informacion para que se escriban los datos en el archivo

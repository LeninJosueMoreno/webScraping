from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
from itemloaders.processors import MapCompose

class Articulo (Item):
    titulo = Field()
    precio = Field()
    descripcion = Field()
    
class MercadoLibreCrawler(CrawlSpider):
    name = 'mercadolibre'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 20
    }
    
    allowed_domains = ['articulo.mercadolibre.com.ec', 'listado.mercadolibre.com.ec']
    
    start_urls = ['https://listado.mercadolibre.com.ec/animales-mascotas/perros/']
    
    download_delay = 2
    
    rules = (
        # Paginacion
        Rule(LinkExtractor(
                allow=r'/_Desde_\d+'
            ), follow=True
        ),
        # Detalle de los productos
        Rule(LinkExtractor(
                allow=r'/MEC-'
            ), 
            follow=True, 
            callback='parse_items'
        ),
    )
    
    def parse_items(self, response):
        item = ItemLoader(Articulo(), response)
        
        item.add_xpath('titulo', '//h1/text()', MapCompose(lambda i: i.replace('\n', '').replace('\r', '').strip()))
        item.add_xpath('descripcion', '//div[@class="ui-pdp-description"]/p/text()', MapCompose(lambda i: i.replace('\n', '').replace('\r', '').strip())) 
        soup = BeautifulSoup(response.body)
        precio = soup.find(class_="andes-money-amount__fraction")
        precio_completo = precio.text.replace('\n', ' ').replace('\r', ' ').replace(' ', '')
        item.add_value('precio', precio_completo)
        yield item.load_item()


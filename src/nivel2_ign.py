from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Articulo (Item):
    titulo = Field()
    contenido = Field()
    
class Review (Item):
    titulo = Field()
    fecha_de_publicacion = Field()

class Video (Item):
    titulo = Field()
    fecha_de_publicacion = Field()
    
class IGNCrawler (CrawlSpider):
    name = "ign"
    ustom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 100, # Un poco alto
        'FEED_EXPORT_FIELDS': ['titulo', 'fecha_de_publicacion', 'contenido'],
        'FEED_EXPORT_ENCODING': 'utf-8' # Para que se muestren bien los caracteres especiales (ej. acentos)
    }
    
    allowed_domains = ['latam.ign.com']
    start_urls = ['https://latam.ign.com/se/?model=article&q=ps5']
    
    download_delay = 1
    
    rules = (
        Rule(LinkExtractor(allow=r'type='), follow=True),
        Rule(LinkExtractor(allow=r''), callback=''),
        
        )

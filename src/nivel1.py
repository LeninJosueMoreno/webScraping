import requests
from lxml import html

encavezados = {
"user-agent"  : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}
url = "https://www.wikipedia.org/"

respuesta = requests.get(url, headers=encavezados)

parser = html.fromstring(respuesta.text)

idiomas = parser.find_class('central-featured-lang')

for idioma in idiomas:
    print(idioma.text_content())






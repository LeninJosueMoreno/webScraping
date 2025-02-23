import requests
from bs4 import BeautifulSoup

headers = {
"user-agent"  : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

url = "https://stackoverflow.com/questions"

respuesta = requests.get(url,headers= headers)

soup = BeautifulSoup(respuesta.text)

contenedor_de_preguntas = soup.find(id="questions")
lista_de_preguntas = contenedor_de_preguntas.find_all('div',class_ = "s-post-summary")

for pregunta in lista_de_preguntas:

    # METODO #2: APROVECHANDO EL PODER COMPLETO DE BEAUTIFUL SOUP
    contenedor_pregunta = pregunta.find('h3')
    texto_pregunta = contenedor_pregunta.text
    descripcion_pregunta = contenedor_pregunta.find_next_sibling('div')  # TRAVERSANDO EL ARBOL DE UNA MENERA DIFERENTE
    texto_descripcion_pregunta = descripcion_pregunta.text

    texto_descripcion_pregunta = texto_descripcion_pregunta.replace('\n', '').replace('\t', '')
    print (texto_pregunta)
    print (texto_descripcion_pregunta)
    # print ()

import os
from importlib.metadata import metadata

import requests
from bs4 import BeautifulSoup
import csv

url = "https://news.ycombinator.com/"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
}

# Hacemos el requerimiento a la web
respuesta = requests.get(url, headers=headers)

# Verificamos que obtenemos codigo 200
print(respuesta)

# Cargamos el arbol HTML en beautifoul soup
soup = BeautifulSoup (respuesta.text, 'lxml')

# Obtenemos todas las noticias
lista_de_noticias = soup.find_all('tr', class_='athing submission')

# Guardamos en un archivo CSV
f = open('archivo_de_salida.csv','w')
escritor = csv.writer(f)

# Por cada noticia en la lista de noticias
for noticia in lista_de_noticias:
    # Obtenemos el titulo de la noticia
    titulo = noticia.find('span', class_='titleline').text

    # Obtenemos la URL a la que redirige al darle click a la noticia
    url = noticia.find('span',class_='titleline').find('a').get('href')
    score = 0
    comentarios = 0
    metadata= noticia.find_next_sibling()

    try:
        score_tmp = metadata.find('span',class_='score').text
        score_tmp = score_tmp.replace('points', '').strip()
        score = int(score_tmp)
    except Exception as e:
        print(e)
        print('No se encontro score')

    try:
        subline = metadata.find(attrs={'class': 'subline'}).text
        info = subline.strip('|')
        comentarios_tmp = info[-1]
        comentarios_tmp = comentarios_tmp.replace('comments', '').strip()
        comentarios = int(comentarios_tmp)
    except:
        print('No hay comentarios')

    escritor.writerow([titulo, url, score, comentarios,])
    print(titulo)
    print(url)
    print(score)
    print(comentarios)
    print()

f.close()

ruta_absoluta = os.path.abspath('archivo_de_salida.csv')
print(f"El archivo CSV se guardó en: {ruta_absoluta}")


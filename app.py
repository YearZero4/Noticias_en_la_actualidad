import requests, re, os
from bs4 import BeautifulSoup as b

import unidecode
def quitar_acentos(texto):
 return unidecode.unidecode(texto)

urls = ['https://laverdaddevargas.com/category/sucesos/', 'https://laverdaddevargas.com/category/regionales/', 'https://www.globovision.com/', 'https://cnnespanol.cnn.com/']
datos = []
n=1
for i in urls:
 if n == 1:
  r = requests.get(i)
  soup = b(r.content, 'html.parser')
  bx = soup.find_all('a', rel="bookmark")
  for i in bx:
   ii = str(i)
   find = re.search('datetime', ii)
   if find == None:
    enlace = i['href']
    noticia = i.text
    datos.append(f'<a href="{enlace}">{noticia}</a>\n')
 elif n == 2:
  r = requests.get(i)
  soup = b(r.content, 'html.parser')
  bx = soup.find_all('a', rel="bookmark")
  for i in bx:
   ii = str(i)
   find = re.search('datetime', ii)
   if find == None:
    enlace = i['href']
    noticia = quitar_acentos(i.text)
    datos.append(f'<a href="{enlace}">{noticia}</a>\n')
 elif n == 3:
  url = i
  peticion = requests.get(url)
  soup = b(peticion.content, 'html.parser')
  buscar = soup.find_all('a')
  for d in buscar:
   div = d.find('div', class_='titulo-peq')
   if div:
    for info in div:
     notice = ' '.join(info.text.replace('(+Video)', '').split())
     link = d['href'], div.get_text(strip=True)
     url = list(link)[0]
     noticia = quitar_acentos(notice)
     datos.append(f'<a href="{url}">{noticia}</a>\n')
 elif n == 4:
  peticion = requests.get(i)
  soup = b(peticion.content, 'html.parser')
  buscar = soup.find_all('span',  class_="container__headline-text")
  for d in buscar:
   rango = len(d.text.split())
   if rango > 4:
    datos.append(quitar_acentos(d.text) + '\n')
 n+=1


from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')
def index():
 return render_template('index.html', noticias=datos)
if __name__ == "__main__":
 app.run(debug=True, host="0.0.0.0", port=os.getenv("PORT", default=5000))




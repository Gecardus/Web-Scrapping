import requests 
from bs4 import BeautifulSoup
import sqlite3
conn=sqlite3.connect("animeflv.db")

cursor=conn.cursor()

SQL="CREATE TABLE IF NOT EXISTS animes (nombre TEXT,descripcion TEXT, estado TEXT, genero TEXT)"
SQL2="CREATE TABLE IF NOT EXISTS episodios (numero TEXT)"
SQL3="CREATE TABLE IF NOT EXISTS calificaciones (calificacion TEXT, votos TEXT)"

cursor.execute(SQL)
cursor.execute(SQL2)
cursor.execute(SQL3)
url= 'https://www3.animeflv.net/browse'

resposta = requests.get(url)
html=BeautifulSoup(resposta.text,'html.parser')
animes=html.find_all('li')

for anime in animes:
    
    titol=anime.find('h3')
    if titol:
        
        #print(titol.text)
        links=anime.find('a')["href"]
        
        
        link=requests.get("https://www3.animeflv.net/"+links)
        html=BeautifulSoup(link.text,'html.parser')

        estado=html.find('span',class_='fa-tv')
        #print(estado.text)
        calificacion=html.find('span',class_="vtprmd")
        #print(calificacion.text)
        votos=html.find('span', id="votes_nmbr")
        #print(votos.text)
        descripcion=anime.find('div', class_='Description')

        generos=html.find('nav', class_="Nvgnrs")
        comentarios=html.find('li',class_="post")
        episodios=html.find('li',class_="fa-play-circle")
        episodio=str(episodios)
        series=[(str(titol.text),str(descripcion.text),str(estado.text),str(generos.text))]
        valoraciones=[(str(calificacion.text),str(votos.text))]
        contador=0
        for e in episodio:
            contador+=1
        str(contador)            

        for s in series:
            cursor.execute("INSERT INTO animes (nombre,descripcion, estado, genero) VALUES(?,?,?,?)",s)
        
        for v in valoraciones:
            cursor.execute("INSERT INTO calificaciones (calificacion, votos) VALUES(?,?)",v)
        
        cursor.execute("INSERT INTO episodios (numero) VALUES(?)", (contador,))



conn.commit()

conn.close()
    

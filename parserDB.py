from time import sleep
import requests
from bs4 import BeautifulSoup
import sqlite3 


#SQL
db = sqlite3.connect('server.db')
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS films (
    id BIGINT,
    name TEXT,
    link TEXT
)""")


#парсинг
for page in range(0,10):
        #разбор страницы на lxml
        url = f"https://www.kinoafisha.info/rating/movies/?page={page}"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'lxml')
        #сбор информации
        films = soup.findAll('div', class_ = "movieItem_info")
        id = 0
        for film in films:
            #сбор информации
            link = film.find("a", class_ = "movieItem_title").get("href")
            name = film.find("a", class_ = "movieItem_title").text
            name = name.replace("'","")
            id = id + 1
            #запись sqlite
            
            sql.execute(f"SELECT name FROM films WHERE name = '{name}'")
            if sql.fetchone() is None:
                sql.execute("INSERT INTO films VALUES (?,?,?)", (id, name, link))
                db.commit()
            else:
                print("уже есть")

        sleep(1)
        for value in sql.execute("SELECT * FROM films"):
            print(value)
        print("данные " + str(page+1) + " страницы загружены")





#парсим данные и заливаем все на sql db 
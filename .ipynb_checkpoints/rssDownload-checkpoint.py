from old.urls import rss_list
import feedparser
import sqlite3
import time

conn = sqlite3.connect('db/RSS.sqlite')
cursor=conn.cursor()

def buscaRSS():
    for i in rss_list:
        feed = feedparser.parse(i[2])
        for entries in feed.entries:
            try:
                inserirRSS(i[1], i[0], entries.title)
            except Exception as e:
                print(i, e)

def inserirRSS(publisher, keyword, title):
     cursor.execute("SELECT id FROM RSS WHERE title = ?", [title])
     data=cursor.fetchone()
     if data is None:
         cursor.execute("INSERT INTO RSS (keyword, publisher, title) VALUES (?,?,?)", [keyword,publisher,title])
         conn.commit()
         print("Inserido: {}".format(title))

while True:
    buscaRSS()
    time.sleep(30)

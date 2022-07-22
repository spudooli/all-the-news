from news import app, db
from flask import render_template
import redis
from datetime import date

r = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)

def getthenews(keyword, limit):
    today = date.today()
    newsday = f'{today.strftime("%Y-%m-%d")} 00:00:00'
    cursor = db.mysql.connection.cursor()
    likeString = f'%{keyword}%'
    cursor.execute("SELECT id, headline, summary, source, url, keywords, section, scrapedate FROM news where keywords like %s and scrapedate > %s order by rand() limit %s", (likeString, newsday, limit))
    newsitems = cursor.fetchall()
    cursor.close()
    return newsitems

@app.route("/")
def index():
    item1 = getthenews("covid", 17)
    item2 = getthenews("terror", 15)
    item3 = getthenews("ukraine", 15)
    item4 = getthenews("luxon", 12)



   



    return render_template('index.html', item1 = item1, item2 = item2, item3 = item3, item4 = item4)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



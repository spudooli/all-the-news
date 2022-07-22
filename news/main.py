from news import app, db
from flask import render_template
import redis
from datetime import date

r = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)

def getthenews(section):
    today = date.today()
    newsday = f'{today.strftime("%Y-%m-%d")} 00:00:00'
    cursor = db.mysql.connection.cursor()
    #cursor.execute("SELECT id, headline, summary, source, url, keywords, section, scrapedate FROM news where keywords like %s and scrapedate > %s order by rand() limit %s", (likeString, newsday, limit))

    cursor.execute("SELECT id, headline, summary, source, url, clusterid, section, scrapedate FROM news where clusterid IS NOT NULL and section = %s order by clusterid", (section,))
    newsitems = cursor.fetchall()
    cursor.close()
    return newsitems

@app.route("/<section>")
def index(section):
    if section == 'business':
        section = 'business'
        item1 = getthenews("business")

    if section == 'technology':
        section = 'technology'
        item1 = getthenews("technology")
    
    if section == 'world':
        section = 'world'
        item1 = getthenews("world")
    
    if section == 'sport':
        section = 'sport'
        item1 = getthenews("sport")

 



    return render_template('index.html', item1 = item1, section = section)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



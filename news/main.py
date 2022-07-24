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

    cursor.execute("SELECT id, headline, summary, source, url, clusterid, section, scrapedate FROM news where clusterid IS NOT NULL and section LIKE %s and scrapedate > %s order by clusterid", (section, newsday))
    newsitems = cursor.fetchall()
    cursor.close()
    return newsitems

def getthenewsagain(section):
    today = date.today()
    newsday = f'{today.strftime("%Y-%m-%d")} 00:00:00'
    cursor = db.mysql.connection.cursor()
    #cursor.execute("SELECT id, headline, summary, source, url, keywords, section, scrapedate FROM news where keywords like %s and scrapedate > %s order by rand() limit %s", (likeString, newsday, limit))

    cursor.execute("SELECT id, headline, summary, source, url, clusterid, section, scrapedate, pubdate FROM news where clusterid IS NOT NULL and section LIKE %s and scrapedate > %s order by clusterid", (section, newsday))
    newsitems = cursor.fetchall()
    
    desc = cursor.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row))  
        for row in newsitems]
    cursor.close()
    return data

@app.route('/', strict_slashes=False, defaults={'section': None} )
@app.route("/<section>")
def index(section):
    if section == 'business':
        section = 'Business'
        item1 = getthenewsagain("business")

    if section == 'technology':
        section = 'Technology'
        item1 = getthenewsagain("technology")
    
    if section == 'world':
        section = 'World'
        item1 = getthenewsagain("world")
    
    if section == 'sport':
        section = 'Sport'
        item1 = getthenewsagain("sport")

    if section == 'politics':
        section = 'Politics'
        item1 = getthenewsagain("politics")
    
    if section is None:
        section = 'NZ News'
        item1 = getthenewsagain("nz")


    return render_template('index.html', item1 = item1, section = section)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



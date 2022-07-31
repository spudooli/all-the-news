from news import app, db
from flask import render_template, redirect
from datetime import date
from datetime import datetime, timedelta


def getthenewsagain(section):
    if section == "business" or section == "technology" or section == "politics" or section == "world":
        newsday = datetime.today() - timedelta(days=3)
        newsday = f'{newsday.strftime("%Y-%m-%d")} 00:00:00'
    elif section == "te ao maori":
        newsday = datetime.today() - timedelta(days=10)
        newsday = f'{newsday.strftime("%Y-%m-%d")} 00:00:00'
    elif section == "sport":
        newsday = datetime.today() - timedelta(days=2)
        newsday = f'{newsday.strftime("%Y-%m-%d")} 00:00:00'
    else:
        today = date.today()
        newsday = f'{today.strftime("%Y-%m-%d")} 00:00:00'
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT id, headline, summary, source, url, clusterid, section, scrapedate, pubdate, featured, clustercount FROM news where clusterid IS NOT NULL and section LIKE %s and scrapedate > %s  order by clustercount DESC, clusterid", (section, newsday))
    newsitems = cursor.fetchall()
    desc = cursor.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row))  
        for row in newsitems]
    cursor.close()
    return data


def getthetrendingitems(keyword):
    newsday = datetime.today() - timedelta(days=10)
    newsday = f'{newsday.strftime("%Y-%m-%d")} 00:00:00'
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT id, headline, summary, source, url, clusterid, section, scrapedate, pubdate, keywords, clustercount FROM news where clusterid IS NOT NULL and keywords LIKE %s and scrapedate > %s", ("%" + keyword + "%", newsday))
    newsitems = cursor.fetchall()
    desc = cursor.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row))  
        for row in newsitems]
    cursor.close()
    return data


def getthelastid():
    # Get the last id out of the database to provide a way to warn there is new content
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT id FROM news order by id desc limit 1")  
    lastid = cursor.fetchone()
    cursor.close()
    return lastid[0]


def getfeatured() :
    # Get the featured/trending news items
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT id, title, url, category FROM featured_news")
    featureditems = cursor.fetchall()
    desc = cursor.description
    column_names = [col[0] for col in desc]
    featured = [dict(zip(column_names, row))  
        for row in featureditems]
    cursor.close()
    return featured


def lastupdated():
    # Get the last updated date
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT scrapedate FROM news order by scrapedate desc limit 1")
    lastupdated = cursor.fetchone()
    cursor.close()
    return lastupdated[0]


@app.route('/', strict_slashes=False, defaults={'section': None} )
@app.route("/<section>")
def index(section):
    if section == 'business':
        section = 'Business'
        item1 = getthenewsagain("business")

    elif section == 'technology':
        section = 'Technology'
        item1 = getthenewsagain("technology")
    
    elif section == 'world':
        section = 'World'
        item1 = getthenewsagain("world")
    
    elif section == 'sport':
        section = 'Sport'
        item1 = getthenewsagain("sport")

    elif section == 'politics':
        section = 'Politics'
        item1 = getthenewsagain("politics")
    
    elif section is None:
        section = 'NZ News'
        item1 = getthenewsagain("nz")

    elif section == 'te-ao-maori':
        section = 'Te Ao Māori'
        item1 = getthenewsagain("te ao maori")

    else:
        return redirect('/', code=301)

    lastid = getthelastid()

    featured = getfeatured()

    lastupdateddate = lastupdated()

    return render_template('index.html', item1 = item1, section = section, lastid = lastid, featured = featured, lastupdateddate = lastupdateddate)


@app.route("/trending/<url>")
def trending(url):

    print(url)

    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT id, keywords, title, url FROM featured_news where url LIKE %s", ("%" + url + "%", ))  
    data = cursor.fetchone()

    keyword = data[1]
    section = data[2]
    item1 = getthetrendingitems(keyword)

    lastid = getthelastid()

    featured = getfeatured()

    lastupdateddate = lastupdated()

    return render_template('index.html', item1 = item1, section = section, lastid = lastid, featured = featured, lastupdateddate = lastupdateddate)


@app.route("/liveupdates/<int:lastid>")
def liveupdates(lastid):
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT id FROM news order by id desc limit 1")  
    currentlastid = cursor.fetchone()
    cursor.close()
    if int(currentlastid[0]) > lastid:
        print("It's bigger")
        return "<a href='/'>Refresh for new news</a>"
    else:
        print("It's not bigger")
        return ""


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    #logging.exception(e)
    app.logger.exception(e)
    return render_template('404.html'), 500
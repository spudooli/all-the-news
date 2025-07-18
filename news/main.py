from news import app, db
from flask import render_template, redirect
from datetime import date
from datetime import datetime, timedelta
from itertools import groupby
from operator import itemgetter


def getthenewsagain(section):
    if section == "business" or section == "politics" or section == "world":
        newsday = datetime.today() - timedelta(days=2)
        newsday = f'{newsday.strftime("%Y-%m-%d")} 00:00:00'
    elif section == "sport":
        newsday = datetime.today() - timedelta(days=2)
        newsday = f'{newsday.strftime("%Y-%m-%d")} 00:00:00'
    else:
        today = date.today()
        newsday = f'{today.strftime("%Y-%m-%d")} 00:00:00'
    cursor = db.mysql.connection.cursor()
    cursor.execute("""
        SELECT id, headline, summary, source, url, clusterid, section, scrapedate, 
               pubdate, featured, clustercount, imageurl, new 
        FROM news 
        WHERE clusterid IS NOT NULL 
          AND section LIKE %s 
          AND scrapedate > %s  
          AND clustercount > 1 
        ORDER BY clusterid
    """, (section, newsday))
    newsitems = cursor.fetchall()
    desc = cursor.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row)) for row in newsitems]
    cursor.close()

    # Group by clusterid
    data.sort(key=itemgetter('clusterid'))  # Ensure sorted for groupby
    grouped = []
    for clusterid, items in groupby(data, key=itemgetter('clusterid')):
        items_list = list(items)
        grouped.append((clusterid, items_list))

    # Sort clusters by clustercount (descending)
    grouped.sort(key=lambda x: x[1][0]['clustercount'], reverse=True)

    return grouped

@app.route('/api/breakingnews')
def api_breakingnews():
    cursor = db.mysql.connection.cursor()
    cursor.execute("""
        SELECT headline, source, url, type
        FROM breaking_news
        ORDER BY id DESC
        LIMIT 10
    """)
    news = cursor.fetchall()
    cursor.close()

    if not news:
        return ""

    html = """
    <div class="breaking-news-block">
        <div class="breaking-news-type">Breaking News</div><br />
    """
    for headline, source, url, type_ in news:
        html += f"""
        <div class="breaking-news-item">
            <a href="{url}" target="_blank">{headline}</a><br />
            <div class="sourcename">{source}</div>
        </div>
        """
    html += "</div>"
    return html

def getthetrendingitems(keyword):
    newsday = datetime.today() - timedelta(days=10)
    newsday = f'{newsday.strftime("%Y-%m-%d")} 00:00:00'
    cursor = db.mysql.connection.cursor()
    cursor.execute("""
                   SELECT id, headline, summary, source, url, clusterid, 
                   section, scrapedate, pubdate, keywords, clustercount 
                   FROM news 
                   WHERE clusterid IS NOT NULL 
                   AND keywords LIKE %s and scrapedate > %s""", ("%" + keyword + "%", newsday))
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


def getfeatured():
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
    cursor.execute(
        "SELECT scrapedate FROM news order by scrapedate desc limit 1")
    lastupdated = cursor.fetchone()
    cursor.close()
    return lastupdated[0]


@app.route('/', strict_slashes=False, defaults={'section': None})
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
    return render_template('index.html', item1=item1, section=section, lastid=lastid, featured=featured, lastupdateddate=lastupdateddate)


@app.route("/trending/<url>")
def trending(url):
    cursor = db.mysql.connection.cursor()
    cursor.execute(
        "SELECT id, keywords, title, url FROM featured_news where url LIKE %s", ("%" + url + "%", ))
    data = cursor.fetchone()
    keyword = data[1]
    section = data[2]
    item1 = getthetrendingitems(keyword)
    lastid = getthelastid()
    featured = getfeatured()
    lastupdateddate = lastupdated()

    return render_template('index.html', item1=item1, section=section, lastid=lastid, featured=featured, lastupdateddate=lastupdateddate)


@app.route("/liveupdates/<int:lastid>")
def liveupdates(lastid):
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT id FROM news order by id desc limit 1")
    currentlastid = cursor.fetchone()
    cursor.close()
    if int(currentlastid[0]) > lastid:
        #print("It's bigger")
        return "<a href='/'>Refresh for new news</a>"
    else:
        #print("It's not bigger")
        return ""

@app.route('/newsstats', strict_slashes=False, defaults={'newssubject': None} )
@app.route("/newsstats/<newssubject>")
def newsstats(newssubject):
    if newssubject is None:
        cursor = db.mysql.connection.cursor()
        cursor.execute("""WITH RECURSIVE months AS (
            SELECT DATE_FORMAT(MIN(scrapedate), '%Y-%m-01') AS month_start FROM news
            UNION ALL
            SELECT DATE_FORMAT(DATE_ADD(month_start, INTERVAL 1 MONTH), '%Y-%m-01')
            FROM months
            WHERE month_start < (SELECT DATE_FORMAT(MAX(scrapedate), '%Y-%m-01') FROM news)
            )
            SELECT 
                DATE_FORMAT(m.month_start, '%b %Y') AS month_year, -- Format for display
                COALESCE(COUNT(s.id), 0) AS news_count -- Ensure missing months show count = 0
            FROM months m
            LEFT JOIN (
                SELECT id, DATE_FORMAT(scrapedate, '%Y-%m-01') AS month_start
                FROM news
                WHERE MATCH(headline) AGAINST('israel' IN NATURAL LANGUAGE MODE)
            ) s ON m.month_start = s.month_start
            GROUP BY m.month_start
            ORDER BY m.month_start""")
        newsstatsdata = cursor.fetchall()
        newsstatslabels = [row[0] for row in newsstatsdata]
        newsstatsvalues = [str(row[1]) for row in newsstatsdata]
        cursor.close() 
        
        cursor = db.mysql.connection.cursor()
        cursor.execute(''' WITH RECURSIVE keyword_split AS (
                -- Base case: Extract the first keyword from each row
                SELECT id, 
                    TRIM(LOWER(SUBSTRING_INDEX(keywords, ',', 1))) AS keyword, 
                    SUBSTRING(keywords, LENGTH(SUBSTRING_INDEX(keywords, ',', 1)) + 2) AS remaining_keywords
                FROM news
                WHERE keywords IS NOT NULL AND keywords <> ''

                UNION ALL

                -- Recursive case: Extract subsequent keywords
                SELECT id, 
                    TRIM(LOWER(SUBSTRING_INDEX(remaining_keywords, ',', 1))), 
                    SUBSTRING(remaining_keywords, LENGTH(SUBSTRING_INDEX(remaining_keywords, ',', 1)) + 2)
                FROM keyword_split
                WHERE remaining_keywords IS NOT NULL AND remaining_keywords <> ''
            )

                SELECT keyword, COUNT(*) AS occurrences
                FROM keyword_split
                WHERE keyword IS NOT NULL AND keyword <> ''
                GROUP BY keyword
                ORDER BY occurrences DESC, keyword ASC
                LIMIT 40''')
        top40news = cursor.fetchall()

    else:
        pass

    return render_template('newsstats.html', newssubject=newssubject, newsstatslabels=newsstatslabels, newsstatsvalues=newsstatsvalues, top40news=top40news)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    # logging.exception(e)
    app.logger.exception(e)
    return render_template('404.html'), 500

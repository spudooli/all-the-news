from news import app, db
from flask import render_template, redirect
from datetime import date
from datetime import datetime, timedelta
from itertools import groupby
from operator import itemgetter
import calendar


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

    # Fetch social posts matching any news URL in this section's results
    all_urls = [item['url'] for _, items_list in grouped for item in items_list]
    social_by_url = {}
    if all_urls:
        placeholders = ', '.join(['%s'] * len(all_urls))
        cursor2 = db.mysql.connection.cursor()
        cursor2.execute(f"""
            SELECT username, user_url, post_url, card_url
            FROM social_news
            WHERE card_url IN ({placeholders})
            ORDER BY created_at DESC
        """, all_urls)
        social_rows = cursor2.fetchall()
        social_desc = cursor2.description
        social_cols = [col[0] for col in social_desc]
        cursor2.close()
        for row in social_rows:
            post = dict(zip(social_cols, row))
            social_by_url.setdefault(post['card_url'], []).append(post)

    # Attach social posts to each cluster
    grouped_with_social = []
    for clusterid, items_list in grouped:
        cluster_social = []
        seen_post_urls = set()
        for item in items_list:
            for post in social_by_url.get(item['url'], []):
                if post['post_url'] not in seen_post_urls:
                    cluster_social.append(post)
                    seen_post_urls.add(post['post_url'])
        grouped_with_social.append((clusterid, items_list, cluster_social))

    return grouped_with_social

def getthenewsonday(section, target_date):
    day_start = f'{target_date.strftime("%Y-%m-%d")} 00:00:00'
    day_end = f'{(target_date + timedelta(days=1)).strftime("%Y-%m-%d")} 00:00:00'
    cursor = db.mysql.connection.cursor()
    cursor.execute("""
        SELECT id, headline, summary, source, url, clusterid, section, scrapedate,
               pubdate, featured, clustercount, imageurl, new
        FROM news
        WHERE clusterid IS NOT NULL
          AND section LIKE %s
          AND scrapedate >= %s
          AND scrapedate < %s
          AND clustercount > 1
        ORDER BY clusterid
    """, (section, day_start, day_end))
    newsitems = cursor.fetchall()
    desc = cursor.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row)) for row in newsitems]
    cursor.close()

    data.sort(key=itemgetter('clusterid'))
    grouped = []
    for clusterid, items in groupby(data, key=itemgetter('clusterid')):
        items_list = list(items)
        grouped.append((clusterid, items_list))

    grouped.sort(key=lambda x: x[1][0]['clustercount'], reverse=True)

    all_urls = [item['url'] for _, items_list in grouped for item in items_list]
    social_by_url = {}
    if all_urls:
        placeholders = ', '.join(['%s'] * len(all_urls))
        cursor2 = db.mysql.connection.cursor()
        cursor2.execute(f"""
            SELECT username, user_url, post_url, card_url
            FROM social_news
            WHERE card_url IN ({placeholders})
            ORDER BY created_at DESC
        """, all_urls)
        social_rows = cursor2.fetchall()
        social_desc = cursor2.description
        social_cols = [col[0] for col in social_desc]
        cursor2.close()
        for row in social_rows:
            post = dict(zip(social_cols, row))
            social_by_url.setdefault(post['card_url'], []).append(post)

    grouped_with_social = []
    for clusterid, items_list in grouped:
        cluster_social = []
        seen_post_urls = set()
        for item in items_list:
            for post in social_by_url.get(item['url'], []):
                if post['post_url'] not in seen_post_urls:
                    cluster_social.append(post)
                    seen_post_urls.add(post['post_url'])
        grouped_with_social.append((clusterid, items_list, cluster_social))

    return grouped_with_social


def _historical_date(years_ago):
    today = date.today()
    target_year = today.year - years_ago
    # Handle Feb 29 on leap years: fall back to Feb 28
    day = min(today.day, calendar.monthrange(target_year, today.month)[1])
    return date(target_year, today.month, day)


@app.route('/on-this-day/1year')
def on_this_day_1year():
    target = _historical_date(1)
    target_dt = datetime(target.year, target.month, target.day)
    item1 = getthenewsonday("nz", target_dt)
    section = f'Aotearoa NZ News — {target.strftime("%-d %B %Y")}'
    featured = getfeatured()
    lastupdateddate = lastupdated()
    return render_template('history.html', item1=item1, section=section, featured=featured, lastupdateddate=lastupdateddate)


@app.route('/on-this-day/3years')
def on_this_day_3years():
    target = _historical_date(3)
    target_dt = datetime(target.year, target.month, target.day)
    item1 = getthenewsonday("nz", target_dt)
    section = f'Aotearoa NZ News — {target.strftime("%-d %B %Y")}'
    featured = getfeatured()
    lastupdateddate = lastupdated()
    return render_template('history.html', item1=item1, section=section, featured=featured, lastupdateddate=lastupdateddate)


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
        section = 'Aotearoa NZ News'
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
    item1 = [(item.get('clusterid'), [item], []) for item in getthetrendingitems(keyword)]
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




@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    # logging.exception(e)
    app.logger.exception(e)
    return render_template('404.html'), 500

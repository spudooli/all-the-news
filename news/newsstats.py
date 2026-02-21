from news import app, db
from flask import render_template
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/newsstats', strict_slashes=False, defaults={'newssubject': None} )
@app.route("/newsstats/<newssubject>")
def newsstats(newssubject):

    if newssubject is None:
        cursor = db.mysql.connection.cursor()

        totalnewsheadlines = r.get('news_totalnewscount')
        totalnewsheadlines = int(totalnewsheadlines)
        totalnewsheadlines = str("{:,}".format(totalnewsheadlines))

        cursor.execute("SELECT source, count(id) FROM news GROUP BY source order by count(id) desc")
        newsbysource = cursor.fetchall()


        cursor.close()
    
        return render_template('newsstats.html', newssubject=newssubject, totalnewsheadlines=totalnewsheadlines, newsbysource=newsbysource)

    else: 
        cursor = db.mysql.connection.cursor()
        cursor.execute("""WITH RECURSIVE months AS (
            SELECT DATE_FORMAT(MIN(scrapedate), '%%Y-%%m-01') AS month_start FROM news
            UNION ALL
            SELECT DATE_FORMAT(DATE_ADD(month_start, INTERVAL 1 MONTH), '%%Y-%%m-01')
            FROM months
            WHERE month_start < (SELECT DATE_FORMAT(MAX(scrapedate), '%%Y-%%m-01') FROM news)
            )
            SELECT 
                DATE_FORMAT(m.month_start, '%%b %%Y') AS month_year, -- Format for display
                COALESCE(COUNT(s.id), 0) AS news_count -- Ensure missing months show count = 0
            FROM months m
            LEFT JOIN (
                SELECT id, DATE_FORMAT(scrapedate, '%%Y-%%m-01') AS month_start
                FROM news
                WHERE MATCH(headline) AGAINST(%s IN NATURAL LANGUAGE MODE)
            ) s ON m.month_start = s.month_start
            GROUP BY m.month_start
            ORDER BY m.month_start""", (newssubject,))
        newsstatsdata = cursor.fetchall()
        newsstatslabels = [row[0] for row in newsstatsdata]
        newsstatsvalues = [str(row[1]) for row in newsstatsdata]
        cursor.close()

        return render_template('newsstats.html', newssubject=newssubject, newsstatslabels=newsstatslabels, 
                            newsstatsvalues=newsstatsvalues)

        # cursor = db.mysql.connection.cursor()
        # cursor.execute(''' WITH RECURSIVE keyword_split AS (
        #         -- Base case: Extract the first keyword from each row
        #         SELECT id, 
        #             TRIM(LOWER(SUBSTRING_INDEX(keywords, ',', 1))) AS keyword, 
        #             SUBSTRING(keywords, LENGTH(SUBSTRING_INDEX(keywords, ',', 1)) + 2) AS remaining_keywords
        #         FROM news
        #         WHERE keywords IS NOT NULL AND keywords <> ''

        #         UNION ALL

        #         -- Recursive case: Extract subsequent keywords
        #         SELECT id, 
        #             TRIM(LOWER(SUBSTRING_INDEX(remaining_keywords, ',', 1))), 
        #             SUBSTRING(remaining_keywords, LENGTH(SUBSTRING_INDEX(remaining_keywords, ',', 1)) + 2)
        #         FROM keyword_split
        #         WHERE remaining_keywords IS NOT NULL AND remaining_keywords <> ''
        #     )

        #         SELECT keyword, COUNT(*) AS occurrences
        #         FROM keyword_split
        #         WHERE keyword IS NOT NULL AND keyword <> ''
        #         GROUP BY keyword
        #         ORDER BY occurrences DESC, keyword ASC
        #         LIMIT 40''')
        # top40news = cursor.fetchall()




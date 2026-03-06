from news import app, db
from flask import render_template, request, jsonify
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/newsstats', strict_slashes=False)
def newsstats():
    cursor = db.mysql.connection.cursor()

    totalnewsheadlines = r.get('news_totalnewscount')
    totalnewsheadlines = int(totalnewsheadlines)
    totalnewsheadlines = str("{:,}".format(totalnewsheadlines))

    cursor.execute("SELECT source, count(id) FROM news GROUP BY source order by count(id) desc")
    newsbysource = cursor.fetchall()
    cursor.close()

    return render_template('newsstats.html', totalnewsheadlines=totalnewsheadlines, newsbysource=newsbysource)


@app.route('/newsstats/chart-data')
def newsstats_chart_data():
    newssubject = request.args.get('q', '').strip()
    if not newssubject:
        return jsonify({'error': 'No search term provided'}), 400

    cursor = db.mysql.connection.cursor()
    cursor.execute("""WITH RECURSIVE months AS (
        SELECT DATE_FORMAT(MIN(scrapedate), '%%Y-%%m-01') AS month_start FROM news
        UNION ALL
        SELECT DATE_FORMAT(DATE_ADD(month_start, INTERVAL 1 MONTH), '%%Y-%%m-01')
        FROM months
        WHERE month_start < (SELECT DATE_FORMAT(MAX(scrapedate), '%%Y-%%m-01') FROM news)
        )
        SELECT
            DATE_FORMAT(m.month_start, '%%b %%Y') AS month_year,
            COALESCE(COUNT(s.id), 0) AS news_count
        FROM months m
        LEFT JOIN (
            SELECT id, DATE_FORMAT(scrapedate, '%%Y-%%m-01') AS month_start
            FROM news
            WHERE MATCH(headline) AGAINST(%s IN NATURAL LANGUAGE MODE)
        ) s ON m.month_start = s.month_start
        GROUP BY m.month_start
        ORDER BY m.month_start""", (newssubject,))
    newsstatsdata = cursor.fetchall()
    cursor.close()

    return jsonify({
        'labels': [row[0] for row in newsstatsdata],
        'values': [row[1] for row in newsstatsdata],
        'subject': newssubject,
    })


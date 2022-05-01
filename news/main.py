from news import app, db
from flask import render_template
import json
import typesense


client = typesense.Client({
  'nodes': [{
    'host': 'localhost', # For Typesense Cloud use xxx.a1.typesense.net
    'port': '8108',      # For Typesense Cloud use 443
    'protocol': 'http'   # For Typesense Cloud use https
  }],
  'api_key': 'aOY37YzmNajlFtblSeCJL87w9DYBbEiBHNhzpqpontc2Ile2',
  'connection_timeout_seconds': 2
})


@app.route("/")
def index():
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT id, headline, summary, source, url, section FROM news limit 5")
    items = cursor.fetchall()
    cursor.close()
    
    section = client.collections['news'].documents.search({
    'q': 'inflation',
    'query_by': 'headline, summary, keywords',
    })

    jsondata = json.dumps(section)
    section=json.loads(jsondata)
    return render_template('index.html', items = items, section = section)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



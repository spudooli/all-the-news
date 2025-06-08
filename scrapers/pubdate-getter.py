from argparse import ArgumentParser
import lxml
import mysql.connector
import requests
import pytz
from datetime import datetime
from bs4 import BeautifulSoup as Soup

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bobthefish",
    database="spudooli_news",
)

def parse_sitemap(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"}
    resp = requests.get(url, headers=headers)
    print("Fetching " + url)

    # we didn't get a valid response, bail
    if 200 != resp.status_code:
        print("not a valid response from " + url)
        return False

    # BeautifulStoneSoup to parse the document
    soup = Soup(resp.content, features="xml")

    # find all the <url> tags in the document
    urls = soup.findAll('url')
    print("Found " + str(len(urls)) + " urls in " + url)

    # no urls? bail
    if not urls:
        print("no urls found in " + url)
        return False

    # storage for later...
    out = []

    cursor = connection.cursor()

    # extract what we need from the url
    for u in urls:
        loc = u.find('loc').string
        if u.find('lastmod'):
            last = u.find('lastmod').string

            mysqlquery = "SELECT id, url FROM news where url = %s"
            cursor.execute(mysqlquery, (loc,))
            newsid = cursor.fetchone()
            try:
                if newsid:
                    print("found " + str(newsid))
                    print(last)
                    local = 'GMT'
                    if "nzherald" in url:
                        dt = datetime.strptime(last, '%Y-%m-%dT%H:%M:%S.%fZ')
                    elif "1news" in url:
                        dt = datetime.strptime(last, '%Y-%m-%dT%H:%M:%S.%fZ')
                    else:
                        dt = datetime.strptime(last, '%Y-%m-%dT%H:%M:%SZ')
                    dt = pytz.timezone(local).localize(dt)
                    nz_dt = dt.astimezone(pytz.timezone('Pacific/Auckland'))
                    publishdate = nz_dt.strftime("%-d %b %Y %H:%M")
                    print("Publish Date " + publishdate)
                    cursor.execute("UPDATE `news` SET `pubdate` = %s WHERE `id` = %s", (publishdate, newsid[0]))
                    connection.commit()
                else:
                    print("nope")
            except TypeError as e:
                print(e)



if __name__ == '__main__':
    options = ArgumentParser()
    options.add_argument('-u', '--url', action='store',
                         dest='url', help='The file contain one url per line')
    args = options.parse_args()
    parse_sitemap(args.url)




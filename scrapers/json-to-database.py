import mysql.connector
import json
import hashlib
import yake
import feedparser
import sys
import ssl

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bobthefish",
    database="spudooli_news",
)

cursor = connection.cursor()

spin = 1
def spinner():
  global spin
  if spin == 1:
    spin = spin + 1
    return "|"
  elif spin == 2:
    spin = spin + 1
    return "/"
  elif spin == 3:
    spin = spin + 1
    return "-"
  elif spin == 4:
    spin = 1
    return "\\"

def keywordextract(text):
    language = "en"
    max_ngram_size = 2
    deduplication_threshold = 0.9
    deduplication_algo = 'seqm'
    windowSize = 1
    numOfKeywords = 4
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(text)
    keywordlist = ''
    for kw, v in keywords:
        keywordlist += kw + ', '
    return keywordlist


def processjson(file):
    with open(file) as f:
        data = json.load(f)
        for item in data:
            sys.stdout.write(spinner())
            sys.stdout.flush()
            sys.stdout.write('\b')
            urlhash = hashlib.md5(item['url'].encode())
            text = item['headline'] + " " + item['summary']
            keywords = keywordextract(text)
            cursor.execute(
                "INSERT IGNORE INTO news (source, section, headline, summary, url, urlhash, keywords, pubdate, imgurl) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (item['source'], item['section'], item['headline'], item['summary'], item['url'], urlhash.hexdigest(), keywords, item['pubdate'], item['imgurl']) ),
            )
            connection.commit()


processjson("/tmp/newshub.json")
processjson("/tmp/rnz.json")
processjson("/tmp/1news.json")
processjson("/tmp/stuff.json")
processjson("/tmp/nzherald.json")

# Delete newsundefinedundefinedundefinedundefinei items that are opinion
print("Deleting the opinion")
cursor.execute(
            "DELETE FROM `news` WHERE `headline` LIKE '%opinion%' OR `summary` LIKE '%OPINION%'", )
connection.commit()

cursor.execute(
            "DELETE FROM `news` WHERE `summary` LIKE '%opinion%' OR `summary` LIKE '%OPINION%'", )
connection.commit()

cursor.execute(
            "DELETE FROM `news` WHERE `summary` LIKE '%sponsored%' OR `summary` LIKE '%SPONSORED%'", )
connection.commit()

# def processrss(url, section):
#     feed = feedparser.parse(url)
#     for entry in feed["entries"]:
#         sys.stdout.write(spinner())
#         sys.stdout.flush()
#         sys.stdout.write('\b')
#         title = entry.get("title")
#         link = entry.get("link")
#         urlhash = hashlib.md5(link.encode())
#         text = title
#         keywords = keywordextract(text)
#         print(".")
#         cursor.execute(
#              "INSERT IGNORE INTO news (source, section, headline, url, urlhash, keywords) VALUES (%s, %s, %s, %s, %s, %s)",
#              ("NBR", section, title, link,  urlhash.hexdigest(), keywords),
#          )
#         connection.commit()

# processrss("https://www.nbr.co.nz/rss.xml", "News")
# processrss("https://www.nbr.co.nz/business/rss", "Business")
# processrss("hhttps://www.nbr.co.nz/tech/rss", "Technology")
# processrss("https://www.nbr.co.nz/politics/rss", "Politics")

connection.close()

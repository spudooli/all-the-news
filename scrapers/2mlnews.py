# -*- mode: Python; tab-width: 2; indent-tabs-mode:nil; -*-          #
######################################################################
# Author: Anton Strilchuk <ype@env.sh>                               #
# URL: http://isoty.pe                                               #
# Created: 07-04-2014                                                #
# Last-Updated: 30-07-2014                                           #
#   By: Anton Strilchuk <ype@env.sh>                                 #
#                                                                    #
# Filename: opml_cluster_agg                                         #
# Version: 0.0.1                                                     #
# Description: Clustering RSS Aggregator                             #
# Based On: Carl Anderson's wonderful Howto @ http://bit.ly/1ioH5pY  #
######################################################################
######################################################################
from xtermcolor import colorize
import mysql.connector
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

import random
import string
import sys
from datetime import date
from datetime import datetime, timedelta

processsection = sys.argv[1]

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bobthefish",
    database="spudooli_news",
)

# Some sections have new news items much slower than others
if processsection == "business" or processsection == "technology" or processsection == "politics" or processsection == "world":
    newsday = datetime.today() - timedelta(days=3)
    newsday = f'{newsday.strftime("%Y-%m-%d")} 00:00:00'
elif processsection == "te ao maori":
        newsday = datetime.today() - timedelta(days=10)
        newsday = f'{newsday.strftime("%Y-%m-%d")} 00:00:00'
elif processsection == "sport":
        newsday = datetime.today() - timedelta(days=2)
        newsday = f'{newsday.strftime("%Y-%m-%d")} 00:00:00'
else:
    today = date.today()
    newsday = f'{today.strftime("%Y-%m-%d")} 00:00:00'

cursor = connection.cursor()
mysqlquery = "SELECT id, headline, summary, source, url, keywords FROM news where section = %s and scrapedate > %s "
cursor.execute(mysqlquery, (processsection, newsday))
items = cursor.fetchall()

# write items to a dfile in /tmp
dfile = open('/tmp/newsitems', 'w')
for item in items:
    dfile.write(str(item))
    dfile.write("\n")
dfile.close()


cursor.close()




# Convert to DataFrame for easy manipulation
df = pd.DataFrame(items, columns=["ID", "Headline", "Summary", "Source", "URL", "Keywords"])

# Combine Headline and Summary for similarity comparison
df["Text"] = df["Headline"] + " " + df["Summary"]

# Compute TF-IDF vectorization
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df["Text"])

# Compute cosine similarity
similarity_matrix = cosine_similarity(tfidf_matrix)

# Threshold for grouping similar articles
threshold = 0.2  # Adjust based on experimentation

# Group items based on similarity
groups = []
visited = set()

for i in range(len(df)):
    if i in visited:
        continue
    group = [i]
    visited.add(i)
    for j in range(len(df)):
        if i != j and j not in visited and similarity_matrix[i][j] > threshold:
            group.append(j)
            visited.add(j)
    groups.append(group)

# Display grouped items
for idx, group in enumerate(groups):
    print(f"Group {idx + 1}:")
    for item in group:
        print(f"  ID: {df.iloc[item]['ID']}, Headline: {df.iloc[item]['Headline']}")
    print()



# # set custerid to null for all news items in the section so we can set a new one
# cursor = connection.cursor()
# mysqlquery = "UPDATE news SET clusterid = NULL where section = %s"
# cursor.execute(mysqlquery, (processsection,))
# connection.commit()


# for key in clusters:
#     print (colorize("|============================================", ansi=10))
#     clusterid = get_random_string(8)
#     for id in clusters[key]:
#         cursor = connection.cursor()

#         # add clusterid to newsitem
#         mysql_insert_query = "update news set clusterid = %s where id = %s"
#         values = (clusterid, newsitemid[id])
#         cursor.execute(mysql_insert_query, values)
#         connection.commit()

#         # Count number of the same clusterid 
#         mysqlquery = "SELECT count(id) as clustercount FROM news where clusterid = %s"
#         cursor.execute(mysqlquery, (clusterid,))
#         clustercount = cursor.fetchone()

#         # and update that count into all matching clusterids so that I can sort by it 
#         # on the news page
#         mysql_insert_query = "update news set clustercount = %s where clusterid = %s"
#         values = (clustercount[0], clusterid)
#         cursor.execute(mysql_insert_query, values)
#         connection.commit()

#         cursor.close()

#         print (colorize ('|', ansi=11)),
#         print (colorize(id, ansi=5)), '\t',
#         print (colorize ('|', ansi=11)),
#         print (colorize(titles[id], ansi=9)),
#         print (colorize(hyperlinks[id], ansi=4)),
#         print (colorize (source[id], ansi=4)),
#         print (colorize (newsitemid[id], ansi=4)),
#         print (colorize (clusterid, ansi=4))

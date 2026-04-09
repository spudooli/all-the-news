import mysql.connector
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from halo import Halo
import random
import string
import sys
from datetime import date
from datetime import datetime, timedelta
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

spinner = Halo(text='Loading', spinner='dots')

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


def totalnewscount():
    cursor = connection.cursor()
    mysqlquery = "SELECT count(id) FROM news"
    cursor.execute(mysqlquery)
    totalnewscount = cursor.fetchone()
    cursor.close()
    r.set('news_totalnewscount', totalnewscount[0])


def processnews(processsection):
    # Some sections have new news items much slower than others
    if processsection == "business" or processsection == "technology" or processsection == "politics" or processsection == "world":
        newsday = datetime.today() - timedelta(days=2)
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
    cursor.close()

    # Convert to DataFrame
    df = pd.DataFrame(items, columns=["ID", "Headline", "Summary", "Source", "URL", "Keywords"])

    # Combine Headline and Summary for similarity analysis
    df["Text"] = df["Headline"] + " " + df["Summary"]

    # Load a pre-trained SentenceTransformer model
    model = SentenceTransformer('all-MiniLM-L6-v2', local_files_only=True)

    # Generate embeddings for the text
    embeddings = model.encode(df["Text"].tolist())

    # Compute cosine similarity between embeddings
    similarity_matrix = cosine_similarity(embeddings)

    # Threshold for grouping
    threshold = 0.4  # Adjust this based on your data

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

    # set clusterid to null for recent news items in the section so we can set a new one
    # (uses the same newsday window — historical clusterids from previous years are preserved)
    cursor = connection.cursor()
    mysqlquery = "UPDATE news SET clusterid = NULL WHERE section = %s AND scrapedate > %s"
    cursor.execute(mysqlquery, (processsection, newsday))
    connection.commit()

    for idx, group in enumerate(groups):
        clusterid = get_random_string(8)
        print(f"Processing Group {clusterid}")
        for item in group:
                # Convert numpy.int64 to native Python int
                news_id = int(df.iloc[item]['ID'])
                
                cursor = connection.cursor()
                mysql_insert_query = "update news set clusterid = %s where id = %s"
                values = (clusterid, news_id)
                cursor.execute(mysql_insert_query, values)
                connection.commit()
                print(f"Processing Group {clusterid}: {df.iloc[item]['Headline']}")

                # Count number of the same clusterid 
                mysqlquery = "SELECT count(id) as clustercount FROM news where clusterid = %s"
                cursor.execute(mysqlquery, (clusterid,))
                clustercount = cursor.fetchone()

                # and update that count into all matching clusterids so that I can sort by it 
                # on the news page
                mysql_insert_query = "update news set clustercount = %s where clusterid = %s"
                values = (clustercount[0], clusterid)
                cursor.execute(mysql_insert_query, values)
                connection.commit()
        print()

    spinner.stop()

if __name__ == "__main__":
    spinner.start()
    spinner.text = f"Getting total news count"
    totalnewscount()
    spinner.text = f"Processing {processsection}"
    processnews(processsection)

    

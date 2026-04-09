import mysql.connector
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import random
import string
import sys
from datetime import datetime, timedelta

if len(sys.argv) < 2:
    print("Usage: python3 historical-mlnews.py YYYY-MM-DD")
    sys.exit(1)

target_date_str = sys.argv[1]
target_date = datetime.strptime(target_date_str, "%Y-%m-%d")
day_start = f'{target_date.strftime("%Y-%m-%d")} 00:00:00'
day_end = f'{(target_date + timedelta(days=1)).strftime("%Y-%m-%d")} 00:00:00'

sections = ["nz"]


def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bobthefish",
    database="spudooli_news",
)


def processsection(section):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id, headline, summary, source, url, keywords FROM news "
        "WHERE section = %s AND scrapedate >= %s AND scrapedate < %s",
        (section, day_start, day_end)
    )
    items = cursor.fetchall()
    cursor.close()

    if not items:
        print(f"No items found for section '{section}' on {target_date_str}")
        return

    df = pd.DataFrame(items, columns=["ID", "Headline", "Summary", "Source", "URL", "Keywords"])
    df["Text"] = df["Headline"] + " " + df["Summary"].fillna("")

    model = SentenceTransformer('all-MiniLM-L6-v2', local_files_only=True)
    embeddings = model.encode(df["Text"].tolist())
    similarity_matrix = cosine_similarity(embeddings)

    threshold = 0.4
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

    # Null out clusterids only for this specific day's articles in this section
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE news SET clusterid = NULL WHERE section = %s AND scrapedate >= %s AND scrapedate < %s",
        (section, day_start, day_end)
    )
    connection.commit()
    cursor.close()

    for group in groups:
        clusterid = get_random_string(8)
        print(f"  [{section}] Group {clusterid} ({len(group)} items)")
        for item in group:
            news_id = int(df.iloc[item]['ID'])
            cursor = connection.cursor()
            cursor.execute("UPDATE news SET clusterid = %s WHERE id = %s", (clusterid, news_id))
            connection.commit()

            cursor.execute("SELECT count(id) FROM news WHERE clusterid = %s", (clusterid,))
            clustercount = cursor.fetchone()[0]
            cursor.execute("UPDATE news SET clustercount = %s WHERE clusterid = %s", (clustercount, clusterid))
            connection.commit()
            cursor.close()


if __name__ == "__main__":
    print(f"Processing historical news for {target_date_str}")
    for section in sections:
        print(f"Processing section: {section}")
        processsection(section)
    print("Done.")

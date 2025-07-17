import json
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bobthefish",
    database="spudooli_news",
)

def update_summaries_from_json(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
        if isinstance(data, list):
            items = data
        else:
            items = [data]

    cursor = connection.cursor()
    updated_count = 0
    for item in items:
        url = item.get("url")
        summary = item.get("summary")
        if url and summary:
            # Check if summary is NULL or empty
            cursor.execute(
                "SELECT summary FROM news WHERE url = %s", (url,)
            )
            result = cursor.fetchone()
            if result and (result[0] is None or result[0].strip() == ""):
                cursor.execute(
                    "UPDATE news SET summary = %s WHERE url = %s",
                    (summary, url)
                )
                updated_count += 1
    connection.commit()
    cursor.close()
    print(f"Updated {updated_count} summaries.")

if __name__ == '__main__':
    update_summaries_from_json("/tmp/stuff-summaries.json")
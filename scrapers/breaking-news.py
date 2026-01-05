import requests
import mysql.connector
import re
import json
from ollama import chat
from ollama import ChatResponse


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "bobthefish",
    "database": "spudooli_news"
}

STUFF_API_URL = "https://www.stuff.co.nz/api/v1.0/stuff/alert"
NZHERALD_API_URL = "https://syndication.nzherald.co.nz/shareddata/newsbar/newsbarscript.js"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
}


def delete_old_alerts():    
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM breaking_news")
    conn.commit()
    cursor.close()
    conn.close()


def fetch_stuff_alerts():
    resp = requests.get(STUFF_API_URL, headers=HEADERS)
    resp.raise_for_status()
    alerts = resp.json()
    # Convert Stuff format to unified format
    formatted = []
    for alert in alerts:
        formatted.append({
            "type": alert.get("type", ""),
            "headline": alert.get("teaser", ""),
            "source": "Stuff",
            "url": alert.get("link", "")
        })
    return formatted


def fetch_nzherald_alerts():
    resp = requests.get(NZHERALD_API_URL, headers=HEADERS)
    resp.raise_for_status()
    # Extract JSON array from JS variable assignment
    match = re.search(r'var sNZHBreakingNews = (\[.*?\]);', resp.text, re.DOTALL)
    if not match:
        return []
    alerts = json.loads(match.group(1))
    # Convert to unified format
    formatted = []
    for alert in alerts:
        formatted.append({
            "type": alert.get("type", ""),
            "headline": alert.get("text", ""),
            "source": "NZ Herald",
            "url": "https://www.nzherald.co.nz" + alert.get("url", "")
        })
    return formatted


def save_alerts(alerts):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    for alert in alerts:
            headline = alert.get("headline", "")
            # Skip if headline contains ':'
            if ":" in headline:
                continue
            score = "1"
            cursor.execute("SELECT id FROM breaking_news WHERE url = %s", (alert["url"],))
            if cursor.fetchone():
                continue
            cursor.execute(
                "INSERT INTO breaking_news (type, headline, source, url, score) VALUES (%s, %s, %s, %s, %s)",
                (
                    alert.get("type", ""),
                    headline,
                    alert.get("source", ""),
                    alert.get("url", ""),
                    score
                )
            )
    conn.commit()
    cursor.close()
    conn.close()


def main():
    stuff_alerts = fetch_stuff_alerts()
    nzherald_alerts = fetch_nzherald_alerts()
    all_alerts = stuff_alerts + nzherald_alerts
    save_alerts(all_alerts)


if __name__ == "__main__":
    delete_old_alerts()
    main()

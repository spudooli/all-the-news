import requests
import time
import mysql.connector

# MySQL connection settings
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'bobthefish',
    'database': 'spudooli_news'
}

MASTODON_URL = "https://mastodon.nz/api/v1/timelines/public?local=true"
NEWS_SITES = ["stuff.co.nz", "nzherald.co.nz", "odt.co.nz", "rnz.co.nz", "tvnz.co.nz"]

def get_db_connection():
    return mysql.connector.connect(**db_config)

def fetch_mastodon_posts():
    resp = requests.get(MASTODON_URL)
    resp.raise_for_status()
    return resp.json()

def save_post_to_db(post):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO social_news (username, user_url, created_at, card_url, post_url)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE id=id
    """
    cursor.execute(sql, (
        post['username'],
        post['user_url'],
        post['created_at'],
        post['card_url'],
        post['post_url']
    ))
    conn.commit()
    cursor.close()
    conn.close()

def main():
    posts = fetch_mastodon_posts()
    for post in posts:
        card = post.get('card')
        if card and card.get('url'):
            card_url = card['url']
            if any(site in card_url for site in NEWS_SITES):
                username = post['account']['username']
                user_url = post['account']['url']
                created_at = post['created_at']
                post_url = post['url']
                print(f"Saving post by {username} at {created_at} with card URL: {card_url}")
                save_post_to_db({
                    'username': username,
                    'user_url': user_url,
                    'created_at': created_at,
                    'card_url': card_url,
                    'post_url': post_url
                })

if __name__ == "__main__":
    main()
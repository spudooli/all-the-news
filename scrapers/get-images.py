import requests
from bs4 import BeautifulSoup
import mysql.connector
from datetime import date
from datetime import datetime, timedelta

def get_og_image(url):
    try:
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        og_image_tag = soup.find('meta', attrs={'property': 'og:image'})
        
        if og_image_tag:
            og_image_url = og_image_tag.get('content')
            return og_image_url
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def update_image_url_in_database(connection, cursor, record_id, og_image_url):
    try:
        update_query = "UPDATE news SET imageurl = %s WHERE id = %s"
        cursor.execute(update_query, (og_image_url, record_id))
        connection.commit()
        print(f"Updated image URL for record with ID {record_id}")
    except Exception as e:
        connection.rollback()
        print(f"An error occurred while updating: {e}")

def main():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="bobthefish",
            database="spudooli_news"
        )
        
        cursor = connection.cursor()

        newsday = datetime.today() - timedelta(days=10)
        newsday = f'{newsday.strftime("%Y-%m-%d")} 00:00:00'
        
        select_query = "SELECT id, url, imageurl FROM news WHERE clusterid IS NOT NULL and source = 'Stuff' and imageurl = '' and scrapedate > %s"
        cursor.execute(select_query, (newsday, ))
        records = cursor.fetchall()
        
        for record in records:
            record_id, url, image_url = record
            og_image_url = get_og_image(url)
            
            if og_image_url:
                update_image_url_in_database(connection, cursor, record_id, og_image_url)
        
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

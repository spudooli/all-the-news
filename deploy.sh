#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

echo "Copying the app..."

cp -p /home/dave/Sites/news/news/* /var/www/news/news/
cp -pr /home/dave/Sites/news/scrapers/* /var/www/news/scrapers/

echo "Deploying the static assets..."

cp -pr /home/dave/Sites/news/news/static/* /var/www/news/news/static/

echo "Deploying the templates..."
cp -rp /home/dave/Sites/news/news/templates/* /var/www/news/news/templates/

echo "Clearing the production cache..."
rm -rf /var/www/news/news/__pycache__

echo "Restarting Gunicorn..."
cd /etc/systemd/system/
systemctl restart news.spudooli.com.service

echo "Done"

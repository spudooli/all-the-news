#!/bin/bash

rm /tmp/stuff-summaries.json
node /var/www/news/scrapers/stuff-summaries.js "https://www.stuff.co.nz/latest-news" nz
python3 /var/www/news/scrapers/update-stuff-summaries.py

rm /tmp/rnz.json
node /var/www/news/scrapers/rnz.js "https://www.rnz.co.nz/news/national" "nz"
node /var/www/news/scrapers/rnz.js "https://www.rnz.co.nz/news/world" "world"
node /var/www/news/scrapers/rnz.js "https://www.rnz.co.nz/news/political" "politics"
node /var/www/news/scrapers/rnz.js "https://www.rnz.co.nz/news/business" "business"
node /var/www/news/scrapers/rnz.js "https://www.rnz.co.nz/news/sport" "sport"
sed -i -e 's/\]\[/\,/g' /tmp/rnz.json
sed -i -e 's/\]undefined\[/\,/g' /tmp/rnz.json

rm /tmp/1news.json
node /var/www/news/scrapers/1news.js "https://www.1news.co.nz/new-zealand/" "nz"
node /var/www/news/scrapers/1news.js "https://www.1news.co.nz/world/" "world"
node /var/www/news/scrapers/1news.js "https://www.1news.co.nz/sport/" "sport"
node /var/www/news/scrapers/1news.js "https://www.1news.co.nz/politics/" "politics"
node /var/www/news/scrapers/1news.js "https://www.1news.co.nz/tags/business/" "business"
node /var/www/news/scrapers/1news.js "https://www.1news.co.nz/sport/rugby/" "sport"
sed -i -e 's/\]\[/\,/g' /tmp/1news.json
sed -i -e 's/\]undefined\[/\,/g' /tmp/1news.json

rm /tmp/stuff.json
node /var/www/news/scrapers/stuff.js "https://www.stuff.co.nz/nz-news" "nz"
node /var/www/news/scrapers/stuff.js "https://www.stuff.co.nz/business" "business"
node /var/www/news/scrapers/stuff.js "https://www.stuff.co.nz/world-news" "world"
node /var/www/news/scrapers/stuff.js "https://www.stuff.co.nz/sport" "sport"
sed -i -e 's/\]\[/\,/g' /tmp/stuff.json
sed -i -e 's/\]undefined\[/\,/g' /tmp/stuff.json

rm /tmp/nzherald.json
node /var/www/news/scrapers/nzherald.js "https://www.nzherald.co.nz/business/" "business"
node /var/www/news/scrapers/nzherald.js "https://www.nzherald.co.nz/politics/" "politics"
node /var/www/news/scrapers/nzherald.js "https://www.nzherald.co.nz/world/" "world"
node /var/www/news/scrapers/nzherald.js "https://www.nzherald.co.nz/sport/" "sport"
node /var/www/news/scrapers/nzherald.js "https://www.nzherald.co.nz/nz/" "nz"
sed -i -e 's/\]\[/\,/g' /tmp/nzherald.json
sed -i -e 's/\]undefined\[/\,/g' /tmp/nzherald.json

rm /tmp/odt.json
node /var/www/news/scrapers/odt.js "https://www.odt.co.nz/news/national" "nz"
node /var/www/news/scrapers/odt.js "https://www.odt.co.nz/business" "business"
node /var/www/news/scrapers/odt.js "https://www.odt.co.nz/news/international" "world"
node /var/www/news/scrapers/odt.js "https://www.odt.co.nz/news/politics" "politics"
sed -i -e 's/\]\[/\,/g' /tmp/odt.json
sed -i -e 's/\]undefined\[/\,/g' /tmp/odt.json


python3 /var/www/news/scrapers/json-to-database.py

python3 /var/www/news/scrapers/3mlnews.py nz
python3 /var/www/news/scrapers/3mlnews.py sport
python3 /var/www/news/scrapers/3mlnews.py world
python3 /var/www/news/scrapers/3mlnews.py politics
python3 /var/www/news/scrapers/3mlnews.py business

 python3 /var/www/news/scrapers/pubdate-getter.py -u "https://www.stuff.co.nz/sitemap.xml"
 python3 /var/www/news/scrapers/pubdate-getter.py -u "https://www.nzherald.co.nz/arc/outboundfeeds/sitemap-news/?outputType=xml&_website=nzh"
 python3 /var/www/news/scrapers/pubdate-getter.py -u "https://www.1news.co.nz/arc/outboundfeeds/news-sitemap/?outputType=xml"

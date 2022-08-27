#!/bin/bash

rm /tmp/rnz.json

node /var/www/news/scrapers/rnz.js "https://www.rnz.co.nz/news/national" "nz"
node /var/www/news/scrapers/rnz.js "https://www.rnz.co.nz/news/world" "world"
node /var/www/news/scrapers/rnz.js "https://www.rnz.co.nz/news/political" "politics"
node /var/www/news/scrapers/rnz.js "https://www.rnz.co.nz/news/business" "business"
node /var/www/news/scrapers/rnz.js "https://www.rnz.co.nz/news/sport" "sport"
# node /var/www/news/scrapers/rnz.js "https://www.rnz.co.nz/news/te-manu-korihi" "te ao maori"

sed -i -e 's/\]\[/\,/g' /tmp/rnz.json
sed -i -e 's/\]undefined\[/\,/g' /tmp/rnz.json

rm /tmp/newshub.json

node /var/www/news/scrapers/newshub.js "https://www.newshub.co.nz/home/new-zealand.html" "nz"
node /var/www/news/scrapers/newshub.js "https://www.newshub.co.nz/home/politics.html" "politics"
node /var/www/news/scrapers/newshub.js "https://www.newshub.co.nz/home/sport.html" "sport"
node /var/www/news/scrapers/newshub.js "https://www.newshub.co.nz/home/money.html" "business"
node /var/www/news/scrapers/newshub.js "https://www.newshub.co.nz/home/technology.html" "technology"
node /var/www/news/scrapers/newshub.js "https://www.newshub.co.nz/home/world.html" "world"


sed -i -e 's/\]\[/\,/g' /tmp/newshub.json
sed -i -e 's/\]undefined\[/\,/g' /tmp/newshub.json


rm /tmp/1news.json

node /var/www/news/scrapers/1news.js "https://www.1news.co.nz/new-zealand/" "nz"
node /var/www/news/scrapers/1news.js "https://www.1news.co.nz/world/" "world"
# node /var/www/news/scrapers/1news.js "https://www.1news.co.nz/sport/" "sport"
node /var/www/news/scrapers/1news.js "https://www.1news.co.nz/politics/" "politics"
node /var/www/news/scrapers/1news.js "https://www.1news.co.nz/tags/business/" "business"
node /var/www/news/scrapers/1news.js "https://www.1news.co.nz/sport/rugby/" "sport"
node /var/www/news/scrapers/1news.js "https://www.1news.co.nz/sport/cricket/" "sport"
node /var/www/news/scrapers/1news.js "https://www.1news.co.nz/sport/motorsport/"

sed -i -e 's/\]\[/\,/g' /tmp/1news.json
sed -i -e 's/\]undefined\[/\,/g' /tmp/1news.json

rm /tmp/stuff.json

node /var/www/news/scrapers/stuff.js "https://www.stuff.co.nz/national/more_headlines" "nz"
node /var/www/news/scrapers/stuff.js "https://www.stuff.co.nz/business/more_headlines" "business"
node /var/www/news/scrapers/stuff.js "https://www.stuff.co.nz/business/money/" "business"
node /var/www/news/scrapers/stuff.js "https://www.stuff.co.nz/world/more_headlines" "world"
node /var/www/news/scrapers/stuff.js "https://www.stuff.co.nz/sport/more_headlines" "sport"
node /var/www/news/scrapers/stuff.js "https://www.stuff.co.nz/technology/more_headlines" "technology"
#node /var/www/news/scrapers/stuff.js "https://www.stuff.co.nz/pou-tiaki" "te ao maori"

sed -i -e 's/\]\[/\,/g' /tmp/stuff.json
sed -i -e 's/\]undefined\[/\,/g' /tmp/stuff.json

rm /tmp/nzherald.json

node /var/www/news/scrapers/nzherald.js "https://www.nzherald.co.nz/business/" "business"
node /var/www/news/scrapers/nzherald.js "https://www.nzherald.co.nz/politics/" "politics"
node /var/www/news/scrapers/nzherald.js "https://www.nzherald.co.nz/world/" "world"
node /var/www/news/scrapers/nzherald.js "https://www.nzherald.co.nz/sport/" "sport"
node /var/www/news/scrapers/nzherald.js "https://www.nzherald.co.nz/nz/" "nz"
node /var/www/news/scrapers/nzherald.js "https://www.nzherald.co.nz/technology/" "technology"
#node /var/www/news/scrapers/nzherald.js "https://www.nzherald.co.nz/kahu/" "te ao maori"

sed -i -e 's/\]\[/\,/g' /tmp/nzherald.json
sed -i -e 's/\]undefined\[/\,/g' /tmp/nzherald.json


rm /tmp/odt.json
node /var/www/news/scrapers/odt.js "https://www.odt.co.nz/news/national" "nz"
node /var/www/news/scrapers/odt.js "https://www.odt.co.nz/business" "business"
node /var/www/news/scrapers/odt.js "https://www.odt.co.nz/news/international" "world"
sed -i -e 's/\]\[/\,/g' /tmp/odt.json
sed -i -e 's/\]undefined\[/\,/g' /tmp/odt.json


python3 /var/www/news/scrapers/json-to-database.py

python3 /var/www/news/scrapers/mlnews.py nz
python3 /var/www/news/scrapers/mlnews.py sport
python3 /var/www/news/scrapers/mlnews.py world
python3 /var/www/news/scrapers/mlnews.py politics
python3 /var/www/news/scrapers/mlnews.py technology
python3 /var/www/news/scrapers/mlnews.py business
# python3 /var/www/news/scrapers/mlnews.py "te ao maori"

python3 /var/www/news/scrapers/pubdate-getter.py -u "https://www.stuff.co.nz/sitemap.xml"
python3 /var/www/news/scrapers/pubdate-getter.py -u "https://www.nzherald.co.nz/arc/outboundfeeds/sitemap-news/?outputType=xml&_website=nzh"
python3 /var/www/news/scrapers/pubdate-getter.py -u "https://www.1news.co.nz/arc/outboundfeeds/news-sitemap/?outputType=xml"

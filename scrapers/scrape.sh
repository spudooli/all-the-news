#!/bin/bash

rm /tmp/rnz.json

node rnz.js "https://www.rnz.co.nz/news/national" "nz"
node rnz.js "https://www.rnz.co.nz/news/world" "world"
node rnz.js "https://www.rnz.co.nz/news/political" "politics"
node rnz.js "https://www.rnz.co.nz/news/business" "business"
node rnz.js "https://www.rnz.co.nz/news/sport" "sport"
node rnz.js "https://www.rnz.co.nz/news/te-manu-korihi" "te ao māori"

sed -i -e 's/\]\[/\,/g' /tmp/rnz.json

rm /tmp/newshub.json

node newshub.js "https://www.newshub.co.nz/home/new-zealand.html" "nz"
node newshub.js "https://www.newshub.co.nz/home/politics.html" "politics"
node newshub.js "https://www.newshub.co.nz/home/sport.html" "sport"
node newshub.js "https://www.newshub.co.nz/home/money.html" "business"
node newshub.js "https://www.newshub.co.nz/home/technology.html" "technology"
node newshub.js "https://www.newshub.co.nz/home/world.html" "world"


sed -i -e 's/\]\[/\,/g' /tmp/newshub.json


rm /tmp/1news.json

node 1news.js "https://www.1news.co.nz/new-zealand/" "nz"
node 1news.js "https://www.1news.co.nz/world/" "world"
# node 1news.js "https://www.1news.co.nz/sport/" "sport"
node 1news.js "https://www.1news.co.nz/politics/" "politics"
node 1news.js "https://www.1news.co.nz/tags/business/" "business"

sed -i -e 's/\]\[/\,/g' /tmp/1news.json


rm /tmp/stuff.json

node stuff.js "https://www.stuff.co.nz/national/more_headlines" "nz"
node stuff.js "https://www.stuff.co.nz/business/more_headlines" "business"
node stuff.js "https://www.stuff.co.nz/business/money/" "business"
node stuff.js "https://www.stuff.co.nz/world/more_headlines" "world"
node stuff.js "https://www.stuff.co.nz/sport/more_headlines" "sport"
node stuff.js "https://www.stuff.co.nz/technology/more_headlines" "technology"
# node stuff.js "https://www.stuff.co.nz/pou-tiaki" "te ao māori"

sed -i -e 's/\]\[/\,/g' /tmp/stuff.json


rm /tmp/nzherald.json

node nzherald.js "https://www.nzherald.co.nz/business/" "business"
node nzherald.js "https://www.nzherald.co.nz/politics/" "politics"
node nzherald.js "https://www.nzherald.co.nz/world/" "world"
node nzherald.js "https://www.nzherald.co.nz/sport/" "sport"
node nzherald.js "https://www.nzherald.co.nz/nz/" "nz"
node nzherald.js "https://www.nzherald.co.nz/technology/" "technology"
node nzherald.js "https://www.nzherald.co.nz/kahu/" "te ao māori"

sed -i -e 's/\]\[/\,/g' /tmp/nzherald.json

python3 json-to-database.py

python3 mlnews.py nz
python3 mlnews.py sport
python3 mlnews.py world
python3 mlnews.py politics
python3 mlnews.py technology
python3 mlnews.py business
python3 mlnews.py "te ao māori"
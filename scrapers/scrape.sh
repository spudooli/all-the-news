#!/bin/bash

rm /tmp/rnz.json

node rnz.js "https://www.rnz.co.nz/news/national"
node rnz.js "https://www.rnz.co.nz/news/world"
node rnz.js "https://www.rnz.co.nz/news/political"
node rnz.js "https://www.rnz.co.nz/news/business"
node rnz.js "https://www.rnz.co.nz/news/sport"

sed -i -e 's/\]\[/\,/g' /tmp/rnz.json

rm /tmp/newshub.json

node newshub.js "https://www.newshub.co.nz/home/new-zealand.html"
node newshub.js "https://www.newshub.co.nz/home/politics.html"
node newshub.js "https://www.newshub.co.nz/home/sport.html"
node newshub.js "https://www.newshub.co.nz/home/money.html"

sed -i -e 's/\]\[/\,/g' /tmp/newshub.json


rm /tmp/1news.json

node 1news.js "https://www.1news.co.nz/new-zealand/"
node 1news.js "https://www.1news.co.nz/world/"
node 1news.js "https://www.1news.co.nz/latest/"

sed -i -e 's/\]\[/\,/g' /tmp/1news.json


rm /tmp/stuff.json

node stuff.js "https://www.stuff.co.nz/national/more_headlines"
node stuff.js "https://www.stuff.co.nz/business/more_headlines"
node stuff.js "https://www.stuff.co.nz/world/more_headlines"
#node stuff.js "https://www.stuff.co.nz/opinion"

sed -i -e 's/\]\[/\,/g' /tmp/stuff.json


rm /tmp/nzherald.json

node nzherald.js "https://www.nzherald.co.nz/business/"
node nzherald.js "https://www.nzherald.co.nz/politics/"
node nzherald.js "https://www.nzherald.co.nz/world/"
node nzherald.js "https://www.nzherald.co.nz/sport/"
node nzherald.js "https://www.nzherald.co.nz/nz/"

sed -i -e 's/\]\[/\,/g' /tmp/nzherald.json

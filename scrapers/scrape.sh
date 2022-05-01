#!/bin/bash

rm /home/dave/Sites/all-the-news/json/rnz.json

node rnz.js "https://www.rnz.co.nz/news/national"
node rnz.js "https://www.rnz.co.nz/news/world"
node rnz.js "https://www.rnz.co.nz/news/political"
node rnz.js "https://www.rnz.co.nz/news/business"
node rnz.js "https://www.rnz.co.nz/news/sport"

sed -i -e 's/\]\[/\,/g' /home/dave/Sites/all-the-news/json/rnz.json

rm /home/dave/Sites/all-the-news/json/newshub.json

node newshub.js "https://www.newshub.co.nz/home/new-zealand.html"
node newshub.js "https://www.newshub.co.nz/home/politics.html"
node newshub.js "https://www.newshub.co.nz/home/sport.html"
node newshub.js "https://www.newshub.co.nz/home/money.html"

sed -i -e 's/\]\[/\,/g' /home/dave/Sites/all-the-news/json/newshub.json


rm /home/dave/Sites/all-the-news/json/1news.json

node 1news.js "https://www.1news.co.nz/new-zealand/"
node 1news.js "https://www.1news.co.nz/world/"
node 1news.js "https://www.1news.co.nz/latest/"

sed -i -e 's/\]\[/\,/g' /home/dave/Sites/all-the-news/json/1news.json


rm /home/dave/Sites/all-the-news/json/stuff.json

node stuff.js "https://www.stuff.co.nz/national/more_headlines"
node stuff.js "https://www.stuff.co.nz/business/more_headlines"
node stuff.js "https://www.stuff.co.nz/world/more_headlines"

sed -i -e 's/\]\[/\,/g' /home/dave/Sites/all-the-news/json/stuff.json


rm /home/dave/Sites/all-the-news/json/nzherald.json

node nzherald.js "https://www.nzherald.co.nz/business/"
node nzherald.js "https://www.nzherald.co.nz/politics/"
node nzherald.js "https://www.nzherald.co.nz/world/"
node nzherald.js "https://www.nzherald.co.nz/sport/"
node nzherald.js "https://www.nzherald.co.nz/nz/"

sed -i -e 's/\]\[/\,/g' /home/dave/Sites/all-the-news/json/nzherald.json

// load in config, puppeteer etc
//const CONFIG = require('./config');
const puppeteer = require('puppeteer');
const url = process.argv[2];
const section = process.argv[3];

void (async () => {

    try {

        const browser = await puppeteer.launch({
            headless: true,
            defaultViewport: {
                width: 1280,
                height: 720
            }
        });

        // create a page inside the browser
        const page = await browser.newPage();
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36');
        
        // navigate to a website
        try {
            await page.goto(url, {
                waitUntil: 'networkidle0'
            });  
        } catch (error) {
            console.log(error);
            browser.close();  
            process.exit();
        }

        let urls = await page.evaluate((section) => {
            let results = [];
            let items = document.querySelectorAll('a.stuff-story-teaser-card');

            try {
                items.forEach((item) => {
                    if (item.querySelector('h5')) {
                        var headline = item.querySelector('h5').innerText;
                    } else {
                        var headline = '';
                    };
                    if (item.querySelector('p')) {
                        var summary = item.querySelector('p').innerText;
                    } else {
                        var summary = '';
                    };
                    if (item.querySelector('img')) {
                        var imgurl = item.querySelector('img').getAttribute("src");
                    } else {
                        var imgurl = '';
                    };
                    if (item.querySelector('time')) {
                        var pubdate = item.querySelector('time').innerText;
                    } else {
                        var pubdate = '';
                    };
                    results.push({
                        source: "Stuff",
                        scrapedate: Date(),
                        section: section,
                        pubdate: pubdate,
                        headline: headline,
                        summary: summary,
                        imgurl: imgurl,
                        //url: 'https://www.stuff.co.nz' + item.querySelector('a').getAttribute("href")
                        url: item.href
                    });
                });
                return results;
            } catch (error) {
                console.log(error);
                browser.close();

            }
        }, section)


        console.log(JSON.stringify(urls, null, 2))

        // save the data as JSON
        const fs = require('fs');

        fs.appendFile(
            '/tmp/stuff.json',
            JSON.stringify(urls, null, 2), // optional params to format it nicely
            (err) => err ? console.error('Data not written!', err) : console.log('Data written!')
        )

        // all done, close this browser
        await browser.close();
    } catch (error) {
        console.log(error);
       browser.close();
    }
})()


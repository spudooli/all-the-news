// load in config, puppeteer etc
//const CONFIG = require('./config');
const puppeteer = require('puppeteer');
const url = process.argv[2];
const section = process.argv[3];

void (async () => {
    // wrapper to catch errors
    try {
        // create a new browser instance
        const browser = await puppeteer.launch({
            args: ['--no-sandbox', '--disable-setuid-sandbox'],
          });
        

        // create a page inside the browser
        const page = await browser.newPage();
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36');

        try {
            await page.goto(url, {
                waitUntil: 'load'
            });  
        } catch (error) {
            console.log(error);
            browser.close();  
            process.exit();
        }
        
        await page.waitForSelector('div.fusion-app');

        let urls = await page.evaluate((section) => {
            let results = [];
            let items = document.querySelectorAll('div.story-card__content');

            try {
                items.forEach((item) => {

                    if (item.querySelector('p.story-card__deck')) {
                        var summary = item.querySelector('p.story-card__deck').innerText;
                    } else {
                        var summary = '';
                    };
                    if (item.querySelector('a').getAttribute("href")) {
                        var url = item.querySelector('a').getAttribute("href");
                    } else {
                        var url = '';
                    };
                    if (item.querySelector('div.story-card__heading-wrapper')) {
                        var headline = item.querySelector('div.story-card__heading-wrapper').innerText;
                    } else {
                        var headline = '';
                    };
                    if (item.querySelector('time')) {
                        var pubdate = item.querySelector('time').innerText;
                    } else {
                        var pubdate = '';
                    };

                    results.push({
                        source: "NZHerald",
                        scrapedate: Date(),
                        pubdate: pubdate,
                        section: section,
                        headline: headline,
                        summary: summary,
                        imgurl: '',
                        url: url
                    });
                });
                return results;
            } catch (error) {
                // if something goes wrong
                // display the error message in console
                console.log(error);
		        browser.close();

            }
        }, section)


        console.log(JSON.stringify(urls, null, 2));

        // save the data as JSON
        const fs = require('fs');

        fs.appendFile(
            '/tmp/nzherald.json',
            JSON.stringify(urls, null, 2), // optional params to format it nicely
            (err) => err ? console.error('Data not written!', err) : console.log('Data written!')
        );

        // all done, close this browser
        await browser.close();
    } catch (error) {
        // if something goes wrong
        // display the error message in console
        console.log(error);
        browser.close();
    }
})()


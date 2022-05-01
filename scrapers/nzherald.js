// load in config, puppeteer etc
//const CONFIG = require('./config');
const puppeteer = require('puppeteer');
const url = process.argv[2];

void (async () => {
    // wrapper to catch errors
    try {
        // create a new browser instance
        const browser = await puppeteer.launch({
            headless: true,
            defaultViewport: {
                width: 1280,
                height: 720
            }
        });

        // create a page inside the browser
        const page = await browser.newPage();
        await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36');

        // navigate to a website
        await page.goto(url, {
            waitUntil: 'load'
        });

        await page.waitForSelector('div.fusion-app');

        let urls = await page.evaluate(() => {
            let results = [];
            let items = document.querySelectorAll('div.story-card__content');

            try {
                items.forEach((item) => {

                    if (item.querySelector('p.story-card__deck')) {
                        var summary = item.querySelector('p.story-card__deck').innerText;
                    } else {
                        var summary = '';
                    };
                    if (item.querySelector('div.story-card__kicker-wrapper')) {
                        var section = item.querySelector('div.story-card__kicker-wrapper').innerText;
                    } else {
                        var section = '';
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

                    results.push({
                        source: "NZHerald",
                        scrapedate: Date(),
                        section: section,
                        headline: headline,
                        summary: summary,
                        url: url
                    });
                });
                return results;
            } catch (error) {
                // if something goes wrong
                // display the error message in console
                console.log(error);
            }
        })


        console.log(JSON.stringify(urls, null, 2));

        // save the data as JSON
        const fs = require('fs');

        fs.appendFile(
            '/home/dave/Sites/all-the-news/json/nzherald.json',
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


// load in config, puppeteer etc
//const CONFIG = require('./config');
const puppeteer = require('puppeteer')
const url = process.argv[2];
const section = process.argv[3];

void (async () => {
    // wrapper to catch errors
    try {
        // create a new browser instance
        const browser = await puppeteer.launch({
            headless: true
        })

        // create a page inside the browser
        const page = await browser.newPage();
        await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36');

        // navigate to a website
        await page.goto(url, {
            waitUntil: 'load'
        });
        let urls = await page.evaluate((section) => {
            let results = [];
            let items = document.querySelectorAll('div.c-NewsTile');

            try {
                items.forEach((item) => {
                    if (item.querySelector('h3')) {
                        headline = item.querySelector('h3').innerText;
                    }
                    if (item.querySelector('h2')) {
                        headline = item.querySelector('h2').innerText;
                    }
                    results.push({
                        source: "Newshub",
                        scrapedate: Date(),
                        pubdate: '',
                        section: section,
                        headline: headline,
                        summary: '',
                        url: item.querySelector('a').getAttribute("href")
                    });
                });
                return results;
            } catch (error) {
                // if something goes wrong
                // display the error message in console
                console.log(error);
            }
        }, section)


        console.log(JSON.stringify(urls, null, 2));

        // save the data as JSON
        const fs = require('fs');

        fs.appendFile(
            '/tmp/newshub.json',
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


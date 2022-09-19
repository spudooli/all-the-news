// load in config, puppeteer etc
//const CONFIG = require('./config');
const puppeteer = require('puppeteer');
const url = process.argv[2];
const section = process.argv[3];

// this wrapper means immediately execute this code
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
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36');
        // navigate to a website
        await page.goto(url, {
            waitUntil: 'load'
        });

        let urls = await page.evaluate((section) => {
            let results = [];
            let items = document.querySelectorAll('div.display-asset');

            try {
                items.forEach((item) => {
                    if (item.querySelector('h3')) {
                        var headline = item.querySelector('h3').innerText;
                    } else {
                        var headline = '';
                    };
                    if (item.querySelector('p.intro-content')) {
                        var summary = item.querySelector('p.intro-content').innerText;
                    } else {
                        var summary = '';
                    };
                    if (item.querySelector('img')) {
                        var imgurl = item.querySelector('img').getAttribute("src");
                    } else {
                        var imgurl = '';
                    };
                    results.push({
                        source: "Stuff",
                        scrapedate: Date(),
                        section: section,
                        pubdate: '',
                        headline: headline,
                        summary: summary,
                        imgurl: '',
                        url: 'https://www.stuff.co.nz' + item.querySelector('a').getAttribute("href")
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
        // if something goes wrong
        // display the error message in console
        console.log(error);
        browser.close();
    }
})()


// load in config, puppeteer etc
//const CONFIG = require('./config');
const puppeteer = require('puppeteer')
const url = process.argv[2];
const section = process.argv[3];

// this wrapper means immediately execute this code
void (async () => {
    // wrapper to catch errors
    try {
        // create a new browser instance
        const browser = await puppeteer.launch({
            headless: true
        });

        // create a page inside the browser
        const page = await browser.newPage();
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36');


        // navigate to a website
        await page.goto(url, {
            waitUntil: 'networkidle2'
        });
        let urls = await page.evaluate((section) => {
            let results = [];
            let items = document.querySelectorAll('li.o-digest');

            try {
                items.forEach((item) => {
		   if (item.querySelector('span.o-kicker__time')) {
                        var pubdate = item.querySelector('span.o-kicker__time').innerText;
                    } else {
                        var pubdate = '';
                    };

                    results.push({
                        source: "RNZ",
                        scrapedate: Date(),
                        pubdate: pubdate,
                        section: section,
                        headline: item.querySelector('h3').innerText,
                        summary: item.querySelector('div.o-digest__summary').innerText,
                        imgurl: item.querySelector('img').getAttribute("src"),
                        url: 'https://www.rnz.co.nz' + item.querySelector('a').getAttribute("href")
                    });
                });
                return results;
            } catch (error) {
                // if something goes wrong
                // display the error message in console
                console.log(error);
            }
        }, section)


        console.log(JSON.stringify(urls, null, 2))

        // save the data as JSON
        const fs = require('fs');

        fs.appendFile(
            '/tmp/rnz.json',
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


// load in config, puppeteer etc
//const CONFIG = require('./config');
const puppeteer = require('puppeteer');
const url = process.argv[2];

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
        await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36');
        // navigate to a website
        await page.goto(url, {
            waitUntil: 'load'
        });
        
        let urls = await page.evaluate(() => {
            section = document.querySelector('h1').innerText;
            let results = [];
            let items = document.querySelectorAll('div.display-asset');

            try {
                items.forEach((item) => {

                    results.push({
                        source: "Stuff",
                        scrapedate: Date(),
                        section: section,
                        headline: item.querySelector('h3').innerText,
                        summary: item.querySelector('p.intro-content').innerText,
                        url: 'https://www.stuff.co.nz' + item.querySelector('a').getAttribute("href")
                    });
                });
                return results;
            } catch (error) {
                // if something goes wrong
                // display the error message in console
                console.log(error);
            }
        })


        console.log(JSON.stringify(urls, null, 2))

        // save the data as JSON
        const fs = require('fs');

        fs.appendFile(
            '/home/dave/Sites/all-the-news/json/stuff.json',
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


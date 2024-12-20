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
            args: ['--no-sandbox', '--disable-setuid-sandbox'],
          });
        

        // create a page inside the browser
        const page = await browser.newPage();
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36');

        // navigate to a website
        try {
            await page.goto(url, {
                waitUntil: 'networkidle2'
            });  
        } catch (error) {
            console.log(error);
            browser.close();  
            process.exit();
        }
        
        let urls = await page.evaluate((section) => {
            let results = [];
            let items = document.querySelectorAll('div.storyItemContainer');

            try {
                items.forEach((item) => {
                    if (item.querySelector('p.testTimeStamp')) {
                        var pubdate = item.querySelector('p.testTimeStamp').innerText;
                    } else {
                        var pubdate = '';
                    };
                    results.push({
                        source: "1 News",
                        scrapedate: Date(),
                        section: section,
                        pubdate: pubdate,
                        headline: item.querySelector('h3').innerText,
                        summary: item.querySelector('p.description').innerText,
                        imgurl: "",
                        // imgurl: item.querySelector('img').getAttribute("src"),
                        url: 'https://www.1news.co.nz' + item.querySelector('a').getAttribute("href")
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
            '/tmp/1news.json',
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


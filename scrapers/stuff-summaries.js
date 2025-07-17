// load in config, puppeteer etc
//const CONFIG = require('./config');
const puppeteer = require('puppeteer');
const url = process.argv[2];
const section = process.argv[3];

void (async () => {

    try {
        const browser = await puppeteer.launch({
            args: ['--no-sandbox', '--disable-setuid-sandbox'],
          });
        // create a page inside the browser
        const page = await browser.newPage();
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36');
        
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
            let items = document.querySelectorAll('div.story-card');

            try {
                items.forEach((item) => {
                    if (item.querySelector('p')) {
                        var summary = item.querySelector('p').innerText;
                    } else {
                        var summary = '';
                    };
                    var link = item.querySelector('a');
                    if (link && link.getAttribute("href")) {
                        var url = link.getAttribute("href");
                    } else {
                        var url = '';
                    }
                    results.push({
                        source: "Stuff",
                        scrapedate: Date(),
                        summary: summary,
                        url: 'https://www.stuff.co.nz' + url
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
            '/tmp/stuff-summaries.json',
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


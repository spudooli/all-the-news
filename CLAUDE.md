# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A New Zealand news aggregator (news.spudooli.com) that scrapes headlines from RNZ, Stuff, NZ Herald, 1News, and ODT, clusters similar stories together using ML, and serves them via a Flask web app.

## Running the App

```bash
# Development server
flask --app news run

# Production: deployed via Gunicorn + systemd
sudo bash deploy.sh
# then: systemctl restart news.spudooli.com.service
```

## Scraping Pipeline

The full scrape pipeline is orchestrated by `scrapers/scrape.sh`. The stages are:

1. **JS scrapers** (Puppeteer) — scrape each news site and append JSON to `/tmp/<source>.json`
   ```bash
   node scrapers/rnz.js "https://www.rnz.co.nz/news/national" "nz"
   node scrapers/stuff.js "https://www.stuff.co.nz/nz-news" "nz"
   # etc.
   ```
2. **JSON to DB** — reads `/tmp/*.json`, extracts keywords with YAKE, inserts into MySQL
   ```bash
   python3 scrapers/json-to-database.py
   ```
3. **ML clustering** — uses `sentence-transformers` (`all-MiniLM-L6-v2`) + cosine similarity to group related stories, writes `clusterid`/`clustercount` back to DB. Takes a section argument:
   ```bash
   python3 scrapers/3mlnews.py nz
   python3 scrapers/3mlnews.py sport
   # sections: nz, sport, world, politics, business
   ```
4. **Breaking news** — fetches live alerts from Stuff API and NZ Herald JS feed:
   ```bash
   python3 scrapers/breaking-news.py
   ```
5. **Pub date getter** — enriches records with publication dates from sitemaps:
   ```bash
   python3 scrapers/pubdate-getter.py -u "https://www.stuff.co.nz/sitemap.xml"
   ```

## Architecture

### Flask App (`news/`)
- `news/__init__.py` — creates the Flask `app` instance
- `news/db.py` — initialises `flask_mysqldb` MySQL connection (database: `spudooli_news`)
- `news/main.py` — all routes: `/`, `/<section>`, `/trending/<url>`, `/liveupdates/<lastid>`, `/api/breakingnews`
- `news/newsstats.py` — `/newsstats` route, uses Redis for cached total count
- Templates in `news/templates/`: `base.html`, `index.html`, `newsstats.html`, `404.html`

### Key Data Flow
- News items are stored in MySQL table `news` with fields: `id`, `headline`, `summary`, `source`, `url`, `urlhash` (MD5, used for dedup), `section`, `scrapedate`, `pubdate`, `keywords`, `clusterid`, `clustercount`, `imageurl`, `new`
- The `clusterid` groups related articles; `clustercount` is the size of each cluster
- The homepage shows only articles where `clustercount > 1` (i.e., covered by multiple sources), sorted by cluster size
- `breaking_news` table holds live alerts (cleared and re-fetched each run)
- `featured_news` table holds manually curated trending topics
- Redis stores `news_totalnewscount` set by `3mlnews.py`

### Sections
Valid section slugs: `nz` (default), `business`, `technology`, `world`, `sport`, `politics`, `te-ao-maori`

### JS Scrapers (`scrapers/*.js`)
All use Puppeteer with `--no-sandbox`. Each scraper takes `(url, section)` args and appends JSON to `/tmp/<source>.json`. Multiple runs concatenate arrays, so `scrape.sh` uses `sed` to fix the resulting `][` joins.

## Infrastructure
- **Database**: MySQL, database `spudooli_news`, user `root`, password `bobthefish` (localhost only)
- **Cache**: Redis on localhost:6379, db 0
- **Production path**: `/var/www/news/`
- **Deploy**: `sudo bash deploy.sh` — copies files to production path and restarts the systemd service

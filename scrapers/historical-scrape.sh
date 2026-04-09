#!/bin/bash
python3 /var/www/news/scrapers/historical-mlnews.py $(date -d "1 year ago" +%Y-%m-%d)
python3 /var/www/news/scrapers/historical-mlnews.py $(date -d "3 years ago" +%Y-%m-%d)

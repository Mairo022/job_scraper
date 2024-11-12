# Job Scraper



## Description
Website that shows latest job ads from multiple job advertisement sites with just one click, 
via its backend server that uses web scraping and publicly available API to find latest job ads.



## Why?
I found it to be quite tedious to keep track of latest job ads across websites 
because of the extra clicks, scrolling, and having to memorise last seen ads, so I wanted
something compact and one click away, without anything unnecessary in the way.

## Getting started
### Requirements
- Python 3
- PHP

#### Install Python packages
```bash
pip install bs4 Flask
```



### Running the application

#### Start backend
```bash
python backend/app.py
```

#### Start frontend
```bash
php -S localhost:6001 -t /frontend
```
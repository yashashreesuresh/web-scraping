### Myntra Gadgets Scraper

Uses `scrapy-selenium`. Refer [this](https://github.com/clemfromspace/scrapy-selenium) doc.

Selenium is required to scrape javascript websites.

Uses selenium to automate the task to navigating to all the pages in gadgets section of Myntra and scrapes the details of each product.

#### Steps to deploy to scrapyd

1. Install scrapy daemon by executing `pip3 install scrapyd`.
2. Install scrapy-client byexecuting `pip3 install git+https://github.com/iamumairayub/scrapyd-client.git --upgrade`.
3. Execute `scrapyd` in one terminal.
4. Change `[deploy]` to `[deploy:local] or [deploy:<str>]` in scrapy.cfg.
5. Uncomment the `url` under `[deploy]` in scrapy.cfg.
5. Execute `scrapyd-deploy local` in another terminal.
6. Execute `curl http://localhost:6800/schedule.json -d project=myntra -d spider=gadgets` to start the spider ececution.
7. Execute step 5 and step 6 whenever a change is made in the project to update the same in scrapy daemon.
8. Execute `curl http://localhost:6800/cancel.json -d project=myntra -d job=<job_id>` to stop the running spider.

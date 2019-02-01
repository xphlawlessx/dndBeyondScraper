# DnD Beyond Scraper
Scrapy practice - Learning how to scrape data from a DnD Beyond character sheet.

DnD Beyond is a companion website for the Dungeons and Dragons roleplaying game. It's a highly responsive website that makes heavy use of javascript and css, which makes scraping it interesting. Not only is there a large amount of html attributes to handle but much of the data is loaded through javascript. This made it a great way to try out splashy as well as to learn more about xpath selectors.

Currently this will scrape character name, ability scores, skills and attacks. The `start_urls` variable contains three sample characters, but this should work on any publicly accessible character.

Requires Splashy - follow setup steps here: https://blog.scrapinghub.com/2015/03/02/handling-javascript-in-scrapy-with-splash

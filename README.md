# Sentiment Analysis on online course reviews
## Intro:
This repo contains scripts to scrape Coursera, EdX, Udacity, and Class Central for reviews on online courses. 

Our Scripts follow the following structure:

1. Scrape review data from Coursera, EdX, Udacity, and Class Central.

2. Validate and Clean scraped data (roughly 100k Rows).

3. Apply Sentiment analysis on cleaned data.

4. Apply topic analysis on clean data.

###  Tools Used:
- Vader Sentiment, Selenium, lxml, requests, pandas, numpy.

## How to use:

For an interactive environment, for webscraping, open:
``jupyter lab coursera_url_scrapper.ipynb	scrapeClassCen.ipynb ``

For an interactive review sentiment analysis, open:
``jupyter lab Review_Sentiment_Analysis.ipynb	coursera_reviews_scraper.ipynb ``


### Citation:
```     

Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.

```



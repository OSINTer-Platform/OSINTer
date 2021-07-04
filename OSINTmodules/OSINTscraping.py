#!/usr/bin/python

# Used for sleeping
import time

# Used for determining the path to the geckodriver
from pathlib import Path

# For manipulating lists in a way that's less memory intensive
import itertools

# The profiles mapping the different websites are in json format
import json

# Used to gather the urls from the articles, by reading a RSS feed
import feedparser

# Used for scraping static pages
import requests

# Used for dynamically scraping pages that aren't static
from selenium import webdriver

# Used for running the browser headlessly
from selenium.webdriver.firefox.options import Options

# For parsing html
from bs4 import BeautifulSoup

from OSINTmodules.OSINTmisc import catURL

# Scraping targets is element and class of element in which the target url is stored, and the profileName is prepended on the list, to be able to find the profile again when it's needed for scraping
def scrapeArticleURLs(rootURL, frontPageURL, scrapingTargets, profileName):

    # List for holding the urls for the articles
    articleURLs = [profileName]

    # The raw source of the site
    frontPage = requests.get(frontPageURL)

    # Parsing the source code from the site to a soup
    frontPageSoup = BeautifulSoup(frontPage.content, 'html.parser')

    # Some websites doesn't have a uniqe class for the links to the articles. If that's the case, we have to extract the elements around the link and the extract the link from those
    if scrapingTargets['linkClass'] == "":
        # Looping through the first 10 of the elements that in the profile has been specified by element type and class to contain the links we want. Only first 10 due to same reason in RSSArticleURLs
        for linkContainer in itertools.islice(frontPageSoup.find_all(scrapingTargets['element'], class_=scrapingTargets['class']), 10):

            # The URL specified in the source will ofc be without the domain and http information, so that get's prepended here too by removing the last / from the url since the path also contains one
            articleURLs.append(catURL(rootURL, linkContainer.find('a').get('href')))

    # Others do hovewer have a uniqe class for the links, and here we can just extract those
    else:
        for link in itertools.islice(frontPageSoup.find_all('a', class_=scrapingTargets['linkClass']), 10):
            articleURLs.append(catURL(rootURL, link.get('href')))

    return articleURLs

# Function for scraping a list of recent articles using the url to a RSS feed
def RSSArticleURLs(RSSURL, profileName):
    # Parse the whole RSS feed
    RSSFeed = feedparser.parse(RSSURL)

    # List for holding the urls from the RSS feed
    articleURLs = [profileName]

    # Extracting the urls only, as these are the only relevant information. Also only take the first 10, if more is given to only get the newest articles
    for entry in itertools.islice(RSSFeed.entries, 10):
        articleURLs.append(entry.id)

    return articleURLs

# Function for gathering list of URLs for articles from newssite
def gatherArticleURLs(profiles):

    articleURLs = list()

    for profile in profiles:

        # Parsing the json properly
        profile = json.loads(profile)['source']

        # For those were the RSS feed is useful, that will be used
        if profile['retrivalMethod'] == "rss":
            articleURLs.append(RSSArticleURLs(profile['newsPath'], profile['profileName']))

        # For basically everything else scraping will be used
        elif profile['retrivalMethod'] == "scraping":
            articleURLs.append(scrapeArticleURLs(profile['address'], profile['newsPath'], profile['scrapingTargets'], profile['profileName']))

    return articleURLs

def scrapePageDynamic(pageURL, loadTime=3, headless=True):

    # Setting the options for running the browser driver headlessly so it doesn't pop up when running the script
    driverOptions = Options()
    driverOptions.headless = headless

    # Setup the webdriver with options
    driver = webdriver.Firefox(options=driverOptions, executable_path=Path("./geckodriver").resolve())

    # Actually scraping the page
    driver.get(pageURL)

    # Sleeping a pre-specified time to let the driver actually render the page properly
    time.sleep(loadTime)

    # Getting the source code for the page
    pageSource = driver.page_source

    driver.quit()

    return pageSource

# Function for scraping OG tag from page
def scrapeOGTags(URL):
    pageSource = requests.get(URL)
    if pageSource.status_code != 200:
        print("Error: Status code " + str(pageSource.status_code) + ", skipping URL: " + URL)
        return []
    pageSoup = BeautifulSoup(pageSource.content, 'html.parser')

    OGTags = list()

    for tag in ["og:title", "og:description", "og:image"]:
        OGTags.append(pageSoup.find("meta", property=tag).get('content'))

    return OGTags

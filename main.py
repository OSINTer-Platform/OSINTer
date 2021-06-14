#!/usr/bin/python

# Used for interacting with the file system
import os

# Used both for determing paths to a certain file/directory and opening files for quick reading
from pathlib import Path

# For manipulating lists in a way that's less memory intensive
import itertools

# The profiles mapping the different websites are in json format
import json

# Used to gather the urls from the articles, by reading a RSS feed
import feedparser

# Used for scraping static pages
import requests

# For parsing html
from bs4 import BeautifulSoup

# For checking if string matches regex
import re


# Function for intellegently adding the domain to a relative path on website depending on if the domain is already there
def catURL(rootURL, relativePath):
    if re.match(r"https?:\/\/.*\..*", relativePath):
        return relativePath
    else:
        return rootURL[:-1] + relativePath

# Function for reading all profile files and returning the content in a list
def getProfiles():
    # Listing all the profiles by getting the OS indepentent path to profiles folder and listing files in it
    profileFiles = os.listdir(path=Path("./profiles"))

    # List for holding the information from all the files, so they only have to be read one
    profiles = list()

    # Reading all the different profile files and storing the contents in just created list
    for profile in profileFiles:

        # Stripping any potential trailing or leading newlines
        profiles.append(Path("./profiles/" + profile).read_text().strip())

    return profiles

def RSSArticleURLs(RSSURL):
    # Parse the whole RSS feed
    RSSFeed = feedparser.parse(RSSURL)

    # List for holding the urls from the RSS feed
    articleURLs = list()

    # Extracting the urls only, as these are the only relevant information. Also only take the first 10, if more is given to only get the newest articles
    for entry in itertools.islice(RSSFeed.entries, 10):
        articleURLs.append(entry.id)

    return articleURLs

# Scraping targets is element and class of element in which the target url is stored
def scrapeArticleURLs(rootURL, frontPageURL, scrapingTargets):

    # List for holding the urls for the articles
    articleURLs = list()

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

    return(articleURLs)


def gatherArticleURLs(profiles):

    articleURLs = list()

    for profile in profiles:

        # Parsing the json properly
        profile = json.loads(profile)['source']

        # For those were the RSS feed is useful, that will be used
        if profile['retrivalMethod'] == "rss":
            articleURLs.append(RSSArticleURLs(profile['newsPath']))

        # For basically everything else scraping will be used
        elif profile['retrivalMethod'] == "scraping":
            articleURLs.append(scrapeArticleURLs(profile['address'], profile['newsPath'], profile['scrapingTargets']))

    return articleURLs


gatherArticleURLs(getProfiles())




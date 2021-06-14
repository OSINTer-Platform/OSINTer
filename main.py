#!/usr/bin/python

# Used for interacting with the file system
import os

# Mainly used for sleeping
import time

# Used both for determing paths to a certain file/directory and opening files for quick reading
from pathlib import Path

# For checking if string matches regex
import re

# For filling out the markdown template at last
from string import Template

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

# For converting html to markdown
from markdownify import markdownify


# Function for intellegently adding the domain to a relative path on website depending on if the domain is already there
def catURL(rootURL, relativePath):
    if re.match(r"https?:\/\/.*\..*", relativePath):
        return relativePath
    else:
        return rootURL[:-1] + relativePath

# Function for taking an arbitrary string and convert it into one that can safely be used as a filename and for removing spaces as those can be a headache to deal with
def fileSafeString(unsafeString):
    allowedCharacthers = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    unsafeString = unsafeString.replace(" ", "-")
    safeString = ''.join(c for c in unsafeString if c in allowedCharacthers)
    return safeString


# Function for using the class of a container along with the element type and class of desired html tag (stored in the contentDetails variable) to extract that specific tag. Data is found under the "scraping" class in the profiles.
def locateContent(contentDetails, soup, multiple=False):

    content = list()

    # Getting the html tag that surrounds that tag we are interrested in
    contentContainer = soup.find(class_=contentDetails['containerClass'])

    # We only want the first entry for some things like date and author, but for the text, which is often split up into different <p> tags we want to return all of them
    if multiple:
        return contentContainer.find_all(contentDetails['element'].split(';'), class_=contentDetails['class'])
    else:
        return contentContainer.find(contentDetails['element'], class_=contentDetails['class'])

# Function for reading all profile files and returning the content in a list if given no argument, or for returning the contents of one profile if given an argument
def getProfiles(profileName=""):
    # Listing all the profiles by getting the OS indepentent path to profiles folder and listing files in it
    profileFiles = os.listdir(path=Path("./profiles"))

    if profileName == "":
        # List for holding the information from all the files, so they only have to be read one
        profiles = list()

        # Reading all the different profile files and storing the contents in just created list
        for profile in profileFiles:

            # Stripping any potential trailing or leading newlines
            profiles.append(Path("./profiles/" + profile).read_text().strip())

        return profiles
    else:
        return Path("./profiles/" + profileName + ".profile").read_text().strip()

def RSSArticleURLs(RSSURL, profileName):
    # Parse the whole RSS feed
    RSSFeed = feedparser.parse(RSSURL)

    # List for holding the urls from the RSS feed
    articleURLs = [profileName]

    # Extracting the urls only, as these are the only relevant information. Also only take the first 10, if more is given to only get the newest articles
    for entry in itertools.islice(RSSFeed.entries, 10):
        articleURLs.append(entry.id)

    return articleURLs

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

    return(articleURLs)


def scrapePageDynamic(pageURL, loadTime=5, headless=True):

    # Setting the options for running the browser driver headlessly so it doesn't pop up when running the script
    driverOptions = Options()
    driverOptions.headless = headless

    # Setup the webdriver with options
    driver = webdriver.Firefox(options=driverOptions)

    # Actually scraping the page
    driver.get(pageURL)

    # Sleeping a pre-specified time to let the driver actually render the page properly
    time.sleep(loadTime)

    # Getting the source code for the page
    pageSource = driver.page_source

    driver.quit()

    return pageSource


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

# Function for collecting all the small details from the article (title, subtitle, date and author)
def extractArticleDetails(contentDetails, soup):
    details = list()
    for detail in contentDetails:
        if contentDetails[detail] != "":
            details.append(locateContent(contentDetails[detail], soup).get_text())

    return details

def extractArticleContent(textDetails, soup, clearText=False, delimiter='\n'):
    # Get the list with the <p> tags in it
    textList = locateContent(textDetails, soup, True)

    assembledText = ""

    # Loop through all the <p> tags, extract the text and add them to string with newline in between
    for element in textList:
        if clearText:
            assembledText = assembledText + element.get_text() + delimiter
        else:
            assembledText = assembledText + str(element) + delimiter

    return assembledText

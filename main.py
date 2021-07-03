#!/usr/bin/python

# The name of your obsidian vault
obsidianVault = ""
# The absolute path to your obsidian vault
vaultPath = ""


## Used for interacting with the file system
#import os
#
## Used for determining what os is running the script
#import sys
#
## Mainly used for sleeping
import time
#
## Used both for determing paths to a certain file/directory and opening files for quick reading
#from pathlib import Path
#
## For checking if string matches regex
#import re
#
## For filling out the markdown template at last
#from string import Template
#
## For manipulating lists in a way that's less memory intensive
#import itertools
#
## The profiles mapping the different websites are in json format
import json
#
## Used to gather the urls from the articles, by reading a RSS feed
#import feedparser
#
## Used for scraping static pages
#import requests
#
import selenium
#
## Used for dynamically scraping pages that aren't static
from selenium import webdriver
#
## Used for running the browser headlessly
#from selenium.webdriver.firefox.options import Options
#
## Used for extracting get paramter from URL, for communicating the profile associated with an article
#from urllib import parse
#
## For parsing html
#from bs4 import BeautifulSoup
#
## For generating random numbers for scrambling the article overview
#import random
#
## Used for normalising cleartext from articles
#import unicodedata
#
## Used for scraping web papges in parrallel (multithreaded)
#from concurrent.futures import ThreadPoolExecutor


from OSINTprofiles import getProfiles
import OSINTscraping
import OSINTextract
import OSINTtext
import OSINTfiles
import OSINTlocal
import OSINTtags
import OSINTmisc

def handleSingleArticle(vaultName, vaultPath, profileName, articleSource, articleURL):

    # Load the profile for the article
    currentProfile = json.loads(getProfiles(profileName))

    # Gather the needed information from the article
    articleDetails, articleContent, articleClearText = OSINTextract.extractAllDetails(currentProfile, articleSource)

    # Generate the tags
    articleTags = OSINTtext.generateTags(OSINTtext.cleanText(articleClearText))

    # Create the markdown file
    MDFileName = OSINTfiles.createMDFile(currentProfile['source']['name'], articleURL, articleDetails, articleContent, articleTags)
    OSINTlocal.openInObsidian(vaultName, vaultPath, MDFileName)

# Function for scraping the the news front side, gather a lot of urls for articles and then put them together in an overview
def scrapeAndConstruct():
    articleURLLists = OSINTscraping.gatherArticleURLs(getProfiles())


    OGTagCollection = OSINTtags.collectAllOGTags(articleURLLists)

    # Constructing the article overview HTML file
    OSINTfiles.constructArticleOverview(OSINTtags.scrambleOGTags(OGTagCollection))


def handleBrowserDriver(driver):
    while True:
        try:
            temp = driver.window_handles
            pageSource = driver.page_source
            pageURL = driver.current_url
        except selenium.common.exceptions.WebDriverException as e:
            break
        time.sleep(1)

    currentProfile = OSINTmisc.extractProfileParamater(pageURL)

    # If the script wasn't able to extract the OSINTerProfile parameter it will warn the user, and just skip the rest of the script, effectivly restarting it
    if currentProfile != None:
        if OSINTmisc.checkIfURL(pageURL):
            return pageSource, pageURL, currentProfile
        else:
            raise Exception("Problem, URL: " + str(pageURL))
    else:
        return None, None, None

def main():
    if OSINTmisc.overviewNeedsRefresh("./webFront/overview.html"):
        print("Refreshing article overview")
        scrapeAndConstruct()
    else:
        print("Using existing article overview")

    # Present the article and grap the driver so the source for the article the user navigates to can be scraped.
    driver = OSINTlocal.presentArticleOverview("./webFront/overview.html")

    pageSource, pageURL, currentProfile = handleBrowserDriver(driver)

    # Making sure the script was able to extract the OSINTerProfile, since it otherwise will only return None
    if pageSource == pageURL == currentProfile == None:
        print("It doesn't seem like the page you navigated to contains the URL \"OSINTerProfile\" parameter needed for the script to continue. This could be due to navigating to another article than one of those offered in the overview, but it could also simply be a bug in the script.")
    else:
        handleSingleArticle(obsidianVault, vaultPath, currentProfile, pageSource, pageURL)


# Dump function for just downloading all the articles the program can scrape
def downloadBulk():
    articleURLLists = gatherArticleURLs(getProfiles())

    for URLlist in articleURLLists:
        currentProfile = URLlist.pop(0)
        for url in URLlist:
            handleSingleArticle(obsidianVault, vaultPath, currentProfile, requests.get(url).content, url)
while True:
    OSINTmisc.checkIfObsidianDetailsSet()
    main()
    if input("Exit? [y/N]: ").lower() == "y":
        break

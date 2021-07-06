#!/usr/bin/python3

# Used for creating a connection to the database
import psycopg2

# Used for loading the profile
import json

from OSINTmodules.OSINTprofiles import getProfiles
from OSINTmodules import *

postgresqlPassword = ""

def fromURLToMarkdown(URL, currentProfile, MDFilePath="./"):

    # Scrape the whole article source based on how the profile says
    if currentProfile['scraping']['type'] == "no-action":
        articleSource = OSINTscraping.scrapePageDynamic(URL)
    else:
        raise Exception(profile['source']['name'] + " apparently didn't have a specified way of scraping the articles autonomously, exiting.")

    # Gather the needed information from the article
    articleDetails, articleContent, articleClearText = OSINTextract.extractAllDetails(currentProfile, articleSource)

    # Generate the tags
    articleTags = OSINTtext.generateTags(OSINTtext.cleanText(articleClearText))

    # Create the markdown file
    MDFileName = OSINTfiles.createMDFile(currentProfile['source']['name'], URL, articleDetails, articleContent, articleTags, MDFilePath)

    return MDFileName


def main():
    # Connecting to the database
    conn = psycopg2.connect("dbname=osinter user=postgres password=" + postgresqlPassword)

    articleURLLists = OSINTscraping.gatherArticleURLs(getProfiles())
    OGTagCollection = OSINTtags.collectAllOGTags(articleURLLists)

    # Writting the OG tags to the database and finding those that haven't already been scraped
    articleCollection = OSINTdatabase.writeOGTagsToDB(conn, OGTagCollection, "articles")

    # Looping through the list of articles from specific news site in the list of all articles from all sites
    for articleList in articleCollection:
        currentProfileName = articleList.pop(0)

        # Making sure the folder for storing the markdown files for the articles in exists, will throw exception if not
        OSINTmisc.createNewsSiteFolder(currentProfileName)

        # Loading the profile for the current website
        currentProfile = json.loads(getProfiles(currentProfileName))

        # Creating the path to the article for the news site
        articlePath = "./articles/{}/".format(currentProfileName)

        for articleURL in articleList:
            fromURLToMarkdown(articleURL, currentProfile, articlePath)
            OSINTdatabase.markAsScraped(conn, articleURL)

main()

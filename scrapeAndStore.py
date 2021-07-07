#!/usr/bin/python3

# Used for creating a connection to the database
import psycopg2

# Used for loading the profile
import json

debugMessages = True

from OSINTmodules.OSINTprofiles import getProfiles
from OSINTmodules.OSINTmisc import printDebug
from OSINTmodules import *

postgresqlPassword = ""

def fromURLToMarkdown(URL, currentProfile, MDFilePath="./"):

    printDebug("\n", False)
    # Scrape the whole article source based on how the profile says
    if currentProfile['scraping']['type'] == "no-action":
        printDebug("No-action scraping: " + URL)
        articleSource = OSINTscraping.scrapePageDynamic(URL)
    else:
        raise Exception(profile['source']['name'] + " apparently didn't have a specified way of scraping the articles autonomously, exiting.")

    printDebug("Extracting the details")
    # Gather the needed information from the article
    articleDetails, articleContent, articleClearText = OSINTextract.extractAllDetails(currentProfile, articleSource)

    printDebug("Generating tags")
    # Generate the tags
    articleTags = OSINTtext.generateTags(OSINTtext.cleanText(articleClearText))

    printDebug("Creating the markdown file")
    # Create the markdown file
    MDFileName = OSINTfiles.createMDFile(currentProfile['source']['name'], URL, articleDetails, articleContent, articleTags, MDFilePath)

    return MDFileName


def main():
    # Connecting to the database
    conn = psycopg2.connect("dbname=osinter user=postgres password=" + postgresqlPassword)

    printDebug("Scraping articles from frontpages and RSS feeds")
    articleURLLists = OSINTscraping.gatherArticleURLs(getProfiles())
    printDebug("Collecting the OG tags")
    OGTagCollection = OSINTtags.collectAllOGTags(articleURLLists)

    printDebug("Writting the OG tags to the DB")
    # Writting the OG tags to the database and finding those that haven't already been scraped
    articleCollection = OSINTdatabase.writeOGTagsToDB(conn, OGTagCollection, "articles")

    # Looping through the list of articles from specific news site in the list of all articles from all sites
    for articleList in articleCollection:
        currentProfileName = articleList.pop(0)
        printDebug("Scraping using this profile: " + currentProfileName)

        # Making sure the folder for storing the markdown files for the articles in exists, will throw exception if not
        OSINTmisc.createNewsSiteFolder(currentProfileName)

        # Loading the profile for the current website
        currentProfile = json.loads(getProfiles(currentProfileName))

        # Creating the path to the article for the news site
        articlePath = "./articles/{}/".format(currentProfileName)

        for articleURL in articleList:
            fromURLToMarkdown(articleURL, currentProfile, articlePath)
            OSINTdatabase.markAsScraped(conn, articleURL)

    printDebug("\n---\n", False)

main()

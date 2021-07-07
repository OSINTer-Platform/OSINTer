# For generating random numbers for scrambling the OG tags
import random

# For loading a profile
import json

# Used for substituting characthers from text
import re

# Used for sleeping
import time

# Used for scraping web papges in parrallel (multithreaded)
from concurrent.futures import ThreadPoolExecutor



# Used for loading a specific profile
from OSINTmodules.OSINTprofiles import getProfiles

# Used for scraping the needed OG tags
from OSINTmodules.OSINTscraping import scrapeOGTags



# Function for collecting OG tags from a list of lists with the URLs for different news sites, with the first element in each of the lists in the list being the name of the profile. Will run in parallel
def collectAllOGTags(articleURLLists):
    # The final collection for holding the scraped OG tags
    OGTagCollection = {}

    # A temporary list for storing the futures generated when launching tasks in parallel
    futureList = []

    # Launching a thread pool executor for parallisation
    with ThreadPoolExecutor(max_workers = 30) as executor:

        # Looping through the list of urls scraped from the front page of a couple of news sites
        for URLList in articleURLLists:

            # Getting the name of the current profile, which is stored in the start of each of the lists with URLs for the different news sites
            currentProfile = URLList.pop(0)

            # Appending a list to the futures list, containing two elements: The name of the profile for the scraped article, and the future itself
            futureList.append([currentProfile, executor.submit(collectOGTagsFromNewsSite, currentProfile, URLList)])

        # Looping through all the futures representing the parallel tasks that are running in the background, checking if they are done and then store the result and remove them from the list if they are
        while futureList != []:
            for future in futureList:
                if future[1].done():
                    OGTagCollection[future[0]] = future[1].result()[future[0]]
                    futureList.remove(future)
            time.sleep(0.1)

    return OGTagCollection


# Function used for ordering the OG tags into a dictionary based on source, that can then be used later. Will only gather articles from one news site at a time
def collectOGTagsFromNewsSite(profileName, URLList):

    # Gets the name of the news media
    siteName = json.loads(getProfiles(profileName))['source']['name']

    # Creating the data structure that will store the OG tags
    OGTagCollection = {}
    OGTagCollection[profileName] = []

    # Looping through each URL for the articles, scraping the OG tags for those articles and then adding them to the final data structure
    for URL in URLList:
        OGTags = scrapeOGTags(URL)
        if OGTags != []:
            # If the sitename isn't in the title, it will be added now
            if siteName.lower() not in OGTags[0].lower():
                OGTags[0] += " | " + siteName

            # The title and description will be cleaned for '"' since these can interfere with storing them in the needed arrays in the JS file and then the OG tag details will be written to the final data structure
            OGTagCollection[profileName].append({
                'profile'       : profileName,
                'url'           : URL,
                'title'         : re.sub(r'"', '', OGTags[0]),
                'description'   : re.sub(r'"', '', OGTags[1]),
                'image'         : OGTags[2]
            })

    return OGTagCollection

# Function used for scrambling the OG tags. The reason the URLs isn't simply scrambled before scrapping the OG tags and thereby making the proccess of scramblin them a lot simpler, is that this will scramble the source, but the newest articles will still be first.
def scrambleOGTags(OGTagCollection):
    # The list of the scrambled OG tags that will be returned
    scrambledTags = list()

    # Making sure that we have no empty lists with articles
    for profile in list(OGTagCollection):
        if OGTagCollection[profile] == []:
            del OGTagCollection[profile]

    while OGTagCollection != {}:
        # Choosing a random source (eg. bleepingcomputer or zdnet or something else)
        randomSource = random.choice(" ".join(OGTagCollection).split())

        # Moves the newest article from a random source from the ordered list to the scrambled
        scrambledTags.append(OGTagCollection[randomSource].pop(0))

        # Checks if individual list is empty and removing it if it is
        if OGTagCollection[randomSource] == []:
            del OGTagCollection[randomSource]

    return(scrambledTags)

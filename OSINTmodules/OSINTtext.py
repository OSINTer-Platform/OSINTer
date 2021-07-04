#!/usr/bin/python

# For doing substitution on text
import re

# For removing weird characthers that sometimes exist in text scraped from the internet
import unicodedata

# For counting and finding the most frequently used words when generating tag
from collections import Counter


# Function for taking in text from article (or basically any source) and outputting a list of words cleaned for punctuation, sole numbers, double spaces and other things so that it can be used for text analyssis
def cleanText(clearText):
    # Normalizing the text, to remove weird characthers that sometimes pop up in webarticles
    cleanClearText = unicodedata.normalize("NFKD", clearText)
    # Removing all contractions and "'s" created in english by descriping possession
    cleanClearText = re.sub(r'\'\S*', '', cleanClearText)
    # Remove all characthers that isn't spaces, numbers or letters
    cleanClearText = re.sub(r'[^\w\s-]', ' ', cleanClearText)
    # Remove those words that are only numbers
    cleanClearText = re.sub(r'\s\d*\s', ' ', cleanClearText)
    # Remove line endings
    cleanClearText = re.sub(r'\n', ' ', cleanClearText)
    # Making sure there isn't anywhere with more than one consecutive space
    cleanClearText = re.sub(r'\s\s', ' ', cleanClearText)

    # Converting the cleaned cleartext to a list
    clearTextList = cleanClearText.split(" ")

    return clearTextList

# Function for taking in a list of words, and generating tags based on that. Does this by finding the words that doesn't appear in a wordlist (which means they probably have some technical relevans) and then sort them by how often they're used. The input should be cleaned with cleanText
def generateTags(clearTextList):

    # List containing words that doesn't exist in the wordlist
    uncommonWords = list()

    # Generating set of all words in the wordlist
    wordlist = set(line.strip() for line in open("./wordlist.txt", "r"))

    # Find all the words that doesn't exist in the normal english dictionary (since those are the names and special words that we want to use as tags)
    for word in clearTextList:
        if word.lower() not in wordlist and word != "":
            uncommonWords.append(word)

    # Take the newly found words, sort by them by frequency and take the 10 most used
    sortedByFreq = [word for word in Counter(uncommonWords).most_common(10)]

    # only use those who have 3 mentions or more
    tagList = list()
    for wordCount in sortedByFreq:
        if wordCount[1] > 2:
            tagList.append(wordCount[0])

    return tagList

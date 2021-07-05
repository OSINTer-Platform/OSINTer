#!/usr/bin/python

# For checking if string matches regex
import re

# For checking how long it was sicne a file was modified
import time
import os

# Used for extracting get paramter from URL, for communicating the profile associated with an article
from urllib import parse

from pathlib import Path

try:
    # For checking that the user indeed has the right variables set for the program
    from __main__ import obsidianVault, vaultPath
except:
    pass


def checkIfURL(URL):
    if re.match(r"https?:\/\/.*\..*", URL):
        return True
    else:
        return False

# Function for intellegently adding the domain to a relative path on website depending on if the domain is already there
def catURL(rootURL, relativePath):
    if checkIfURL(relativePath):
        return relativePath
    else:
        return rootURL[:-1] + relativePath

# Function for taking an arbitrary string and convert it into one that can safely be used as a filename and for removing spaces as those can be a headache to deal with
def fileSafeString(unsafeString):
    allowedCharacthers = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    unsafeString = unsafeString.replace(" ", "-")
    safeString = ''.join(c for c in unsafeString if c in allowedCharacthers)
    return safeString

# Function used for extracting the get parameter for the articles used for communicating the profile associated with an article
def extractProfileParamater(URL):
    try:
        parsedURL = parse.urlparse(URL)
        return parse.parse_qs(parsedURL.query)['OSINTerProfile'][0]
    except KeyError:
        return None

# Function checking whether the variables specifying which obsidian vault to use is set
def checkIfObsidianDetailsSet():
    if obsidianVault == "" or vaultPath == "":
        raise Exception("You need to specify which Obsidian vault to use, and the path to it. These details are defined in the very part of the script as variables.")

# Function for determining whether the file presenting the article overview to the user needs to be refreshed, or if the relative old version can be use
def overviewNeedsRefresh(overviewPath):
    # Checking if file exists
    if os.path.exists(Path(overviewPath)):
        # Get last modification date of the article overview file as well as the current time, both in unix time
        modTime = os.path.getmtime(Path(overviewPath))
        currentTime = time.time()
        # Checking if file is more than 2 hours old
        if (currentTime - modTime) > (2 * 60 * 60):
            return True
        else:
            return False
    else:
        return True



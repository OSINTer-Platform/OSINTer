#!/usr/bin/python

# Used for interacting with the file system
import os

# Used both for determing paths to a certain file/directory and opening files for quick reading
from pathlib import Path

# The profiles mapping the different websites are in json format
import json

# Used to gather the urls from the articles, by reading a RSS feed
import feedparser


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



def main():
    profiles = getProfiles()

main()

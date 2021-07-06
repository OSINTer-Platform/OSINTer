# Used for listing files in directory
import os

# Used for handling relative paths
from pathlib import Path


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

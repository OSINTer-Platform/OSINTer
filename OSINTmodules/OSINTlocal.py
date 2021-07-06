import os
import sys
from pathlib import Path
from requests.utils import quote
from selenium import webdriver

def presentArticleOverview(path):

    # Setup preferences for the webdriver that allows rendering of transparent blured elements
    profile = webdriver.FirefoxProfile()
    profile.set_preference("layout.css.backdrop-filter.enabled", True)
    profile.set_preference("gfx.webrender.all", True)

    # Setup the webdriver using the newly set profile and the path for the geckodriver
    driver = webdriver.Firefox(executable_path=Path("./geckodriver").resolve(), firefox_profile=profile)

    # Present the article
    driver.get("file://" + str(Path(path).resolve()))

    # Return the driver so the rest of the program can interact with the session
    return driver

# Function for moving the newly created markdown file into the obsidian vault, and opening it in obsidian
def openInObsidian(vaultName, vaultPath, fileName):
    # Firstly, move the file to the vault
    os.rename(Path(fileName).resolve(), Path(vaultPath + fileName))

    # Then encode vault and filename for url and remove the .md file extension from the file at the same time
    encVaultName = quote(vaultName, safe='')
    encFileName = quote(fileName[:-3], safe='')

    # Construct the URI for opening obsidian:
    URI = "obsidian://open?vault=" + encVaultName + "&file=" + encFileName

    # And lastly open the file in obsidian by using an URI along with the open command for the currently used OS
    platform = sys.platform

    if platform.startswith('linux'):
        openCommand = "xdg-open '" + URI + "'"
    elif platform.startswith('win32'):
        openCommand = "start '" + URI + "'"
    elif platform.startswith('darwin'):
        openCommand = "open '" + URI + "'"
    elif platform.startswith('cygwin'):
        openCommand = "cygstart '" + URI + "'"
    else:
        raise Exception("Unfortunatly, your system isn't support. You should be running a new version of Windows, Mac or Linux.")

    os.system(openCommand)


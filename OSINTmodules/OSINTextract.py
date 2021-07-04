#!/usr/bin/python

# For parsing html
from bs4 import BeautifulSoup


# Function for using the class of a container along with the element type and class of desired html tag (stored in the contentDetails variable) to extract that specific tag. Data is found under the "scraping" class in the profiles.
def locateContent(contentDetails, soup, multiple=False, recursive=True):

    content = list()

    # Getting the html tag that surrounds that tag we are interrested in
    contentContainer = soup.find(class_=contentDetails['containerClass'])

    try:
        # We only want the first entry for some things like date and author, but for the text, which is often split up into different <p> tags we want to return all of them
        if multiple:
            return contentContainer.find_all(contentDetails['element'].split(';'), class_=contentDetails['class'], recursive=recursive)
        else:
            return contentContainer.find(contentDetails['element'], class_=contentDetails['class'], recursive=recursive)
    except:
        return BeautifulSoup("Unknown", "html.parser")

# Function used for removing certain tags with or without class from a soup. Takes in a list of element tag and class in the format: "tag,class;tag,class;..."
def cleanSoup(soup, HTMLTagsAndClasses):
    for TagAndClass in HTMLTagsAndClasses.split(";"):
        for tag in soup.find_all(TagAndClass.split(",")[0], class_=TagAndClass.split(",")[1]):
            tag.decompose()

    return soup


# Function for collecting all the small details from the article (title, subtitle, date and author)
def extractArticleDetails(contentDetails, soup):
    details = list()
    for detail in contentDetails:
        if contentDetails[detail] != "":
            details.append(locateContent(contentDetails[detail], soup).get_text())
        else:
            details.append("Unknown")

    return details

def extractArticleContent(textDetails, soup, clearText=False, delimiter='\n'):

    # Clean the textlist for unwanted html elements
    if textDetails['remove'] != "":
        cleanedSoup = cleanSoup(soup, textDetails['remove'])
        textList = locateContent(textDetails, cleanedSoup, True, (textDetails['recursive'] == 'True'))
    else:
        textList = locateContent(textDetails, soup, True, (textDetails['recursive'] == 'True'))

    # Get a title image too, if specified in the profile
    if textDetails['headerImage'] != "":
        # Extracting the title image
        headerImage = locateContent(textDetails['headerImage'], soup)
        # Inserting it in the existing soup containing the text and other wanted elements, as the first element, if it was possible to extract one
        if headerImage != None:
            textList.insert(0, headerImage)

    if textList == "Unknown":
        raise Exception("Wasn't able to fetch the text for the following soup:" + str(soup))

    assembledText = ""

    # Loop through all the <p> tags, extract the text and add them to string with newline in between
    for element in textList:
        if clearText:
            assembledText = assembledText + element.get_text() + delimiter
        else:
            assembledText = assembledText + str(element) + delimiter

    return assembledText

# Function for scraping everything of relevans in an article
def extractAllDetails(currentProfile, articleSource):

    # Parsing full source code for the article to a soup
    articleSoup = BeautifulSoup(articleSource, 'html.parser')

    articleDetails =    extractArticleDetails(currentProfile['scraping']['details'], articleSoup)
    articleContent =    extractArticleContent(currentProfile['scraping']['content'], articleSoup)
    articleClearText =  extractArticleContent(currentProfile['scraping']['content'], articleSoup, True)

    return articleDetails, articleContent, articleClearText

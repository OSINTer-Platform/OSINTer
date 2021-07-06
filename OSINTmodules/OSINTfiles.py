# Used for handling relative paths
from pathlib import Path

# For filling out template files like html overview template and markdown template
from string import Template

# For converting html to markdown
from markdownify import markdownify

# Used for checking if theres already a query paramter in the url
from urllib import parse

# Used for creating the name of the markdown file in a safe maner
from OSINTmodules.OSINTmisc import fileSafeString

# Function for writing details from a template to a file
def writeTemplateToFile(contentList, templateFile, newFilePath):
    # Open the template for the given file
    with open(Path(templateFile), "r") as source:
        # Read the template file
        sourceTemplate = Template(source.read())
        # Load the template but fill in the values from contentList
        filledTemplate = sourceTemplate.substitute(contentList)
        # Write the filled template to a new file that can then be used
        with open(Path(newFilePath), "w") as newF:
            newF.write(filledTemplate)

# Function for taking in some details about an articles and creating a markdown file with those
def createMDFile(sourceName, sourceURL, articleDetails, articleContent, articleTags, MDFilePath="./"):

    # Define the title
    title = articleDetails[0]

    # Define the subtitle too, if it exist
    if articleDetails[1] != "Unknown":
        subtitle = articleDetails[1]
    else:
        subtitle = ""

    # Convert the link for the article to markdown format
    MDSourceURL = "[article](" + sourceURL + ")"

    # Define the details section by creating markdown list with "+"
    MDDetails = ""
    detailLabels = ["Source: ", "Link: ", "Date: ", "Author: "]
    for i,detail in enumerate([sourceName, MDSourceURL, articleDetails[2], articleDetails[3]]):
        MDDetails += "+ " + detailLabels[i] + detail + '\n'

    # Convert the scraped article to markdown
    MDContent = markdownify(articleContent)

    # And lastly, some tags
    MDTags = "[[" + "]] [[".join(articleTags) + "]] [[" + sourceName + "]]"

    # Creating a structure for the template
    contentList = {
        'title': title,
        'subtitle': subtitle,
        'information': MDDetails,
        'articleContent': MDContent,
        'tags': MDTags
    }

    # Converting the title of the article to a string that can be used as filename and then opening the file in append mode (will create file if it doesn't exist)
    MDFileName = MDFilePath + fileSafeString(articleDetails[0]) + ".md"

    writeTemplateToFile(contentList, "./markdownTemplate.md", MDFileName)

    # Returning the file name, so it possible to open it in obsidian using an URI
    return MDFileName

# Function used for constructing the CSS and HTML needed for the front end used for presenting the users with the different articles
def constructArticleOverview(OGTags):
    HTML = ""
    CSS = ""
    JS = ""
    # The JS variable contains the list for the following variables: articleURLs imageURLs, titles and descriptions. The string hardcoded into these right here is the name of the javascript arrays that each of these list in the JSList will create
    JSList = [["articleURLs"],["imageURLs"],["titles"],["descriptions"]]
    for i,article in enumerate(OGTags):
        # If there's already a paramater in the url it will add the OSINTerProfile parameter with &, otherwise it will simply use ?
        # OSINTerProfile is used when scraping the website, to know what profile is associated with the article the user choose
        URL = article['url'] + ('&' if parse.urlparse(article['url']).query else '?') + "OSINTerProfile=" + article['profile']
        HTML += '<article id="card-' + str(i) + '"><a href="' + URL + '"><h1>' + article['title'] + '</h1></a></article>\n'
        CSS += '#card-' + str(i) + '::before { background-image: url("' + article['image'] + '");}\n'
        JSList[0].append(URL)
        JSList[1].append(article['image'])
        JSList[2].append(article['title'])
        JSList[3].append(article['description'])

    for currentJSList in JSList:
        JS += 'const ' + currentJSList.pop(0) + ' = [ "' + currentJSList.pop(0) + '"' + "".join([(', "' + element + '"') for element in currentJSList]) + ' ]\n'

    # Make template for HTML file
    writeTemplateToFile({'CSS': CSS, 'HTML': HTML}, "./webFront/index.html", "./webFront/overview.html")

    # Make the template for the JS file
    writeTemplateToFile({'variables': JS}, "./webFront/switchOverview.js", "./webFront/script.js")

# OSINTw

## What is OSINTw?
OSINTw is a simple python script designed for simplifying and automating the
parsing and storing of informations obtained from news article from a number of
news sites. The technical details can be found in the last two sections, but in
short OSINTw presents the user with the 10 most recent articles from each of a
list of pre-defined news sites and when the user has read an article of their
choice, the relevant information from the article will be parsed to a markdown
format based in the included template and opened in obsidian for further editing.
Along the way, tags is also generate for the article, based a simple analysis on
the text from the article.

As stated, this was done, not only to automate the proccess of finding the right
articles to read, but also to save the time wasted when copying the right
details from the article to the markdown file, and while this project has been
aimed at using Obsidian for collecting articles regarding cyber security, it can
easily be modified to collect articles from any news site and opening them in
any markdown editor of your choice.

## Setup
1. Install Firefox and Obsidian
2. Clone this repo to local directory and navigate to it
3. Install the python dependencies specified in requirements using the following
   command:
   `pip install -r requirements.txt`
4. Download the [geckodriver](https://github.com/mozilla/geckodriver/releases),
   unpack it and put the executable in the newly cloned directory
6. Edit the variables "obsidianVault" and "vaultPath" in the start of the start
   of main.py to match the name of your obsidian vault, and the absolute path
   to it.
7. Simply run main.py, sit back and relax while the script does the heavy
   lifting for you.


## What is profiles?
To understand the script, an understanding of the profiles that enables this
script to run in the first place is certainly neccessary. Profiles are in short
simply data structured in a JSON format specifying where and what to scrape.
These are custom created on a site to site basis, and since nearly all news
sites have the same structure (more or less) on all of their articles, they're
made to describe some generic rules on where to find given pieces of information
on a page, like in what HTML element with what tag the date is to be found, or
what element is encapsulating the text in the articles.

The goal with the profiles is to be as generic as possible, with the most in
common with each other, to prevent a programming hell of having to program in
every possible edge case that could appear in an article, and instead allow the
script to use a few simple rules for scraping the articles that are the same for
all sites. With that said though there are two different types of profiles, for
two different kinds of websites. The first one is for the sites that offer a
reliable RSS feed which conform to standards. This one is the prefered method,
since it's not only the simplest method for gathering the newest articles from a
site, but oftentimes also the most reliable.

Some site hovewer, does not offer a RSS feed, or maybe they, but it doesn't
conform to the standard. Here classic webscraping of the front page is used to
find the 10 newest articles, and while it does not offer the same reliability as
the RSS feeds, it does allow for gathering of articles from basically any
news site.

## The technical details
So how does OSINTw function? There is a (admittedly quite primitive) flowchart
included in this repo, but if that's not your coup of tea, then here a quick
rundown of the inner functions of OSINTw.

First the script reads the profiles (which also acts as a list of news sites to
scrape) and based on those scrapes the 10 most recent articles, either using
static scraping of the front page or the RSS feed. The reason for only including
the 10 most recent articles, is that a lot of news sites doesn't include more in
their RSS feed or on their front page without any user interaction, and the limit
is kept at 10 to prevent excesive programming of edge cases and worst case a severe
overweight of some sites.

After this the OG (Open Graph) tags for each article is scraped. These are the
title, a description along with an image and the source url for the article are
used a little later, for creating a front end using HTML, CSS and JavaScript for
letting the user choose an article to read. This proccess is done in parallel for
each news site, to prevent it from becoming too slow when adding more profiles.

As stated, these OG tags are then formatet into HTML (and CSS) and injected into
two templates, one for the HTML/CSS and one for the JavaScript, and the newly
created HTML file is rendered in a firefox browser driven by the geckodriver
using the selenium framework. The reason for using the OG tags for presenting
the articles, is that they're designed to give a short introduction to what the
article contains, which is fitting for this usecase.

By clicking one of the articles presentet visually, the user will then be taken
to the article of their choice, and while the user is reading the article, the
script is collecting the source code of the article a long with the url for it
in the background for later use. The pros of using the same browser for scraping
and presenting the article to the user - outside of not having to request the
same webpage twice - is that the script will get the excact code that is seen
visually by the user. This means that even if the article has some dynamic
loading, or possibly a "Read more" button, that would normally come in the way
of normal static webscraping - or sometimes even dynamic scraping - it will not
have an influence here, since everything the user reads will be visible to the
script.

When the user then closes the article, the script gathers the source code for
the article (since this is then the "final" version of the article) along with
the URL for the article. The URL itself is used for two things; First of all
simply for providing a source for the article when parsing it to markdown, but
two; also for specifying which profile to use for scraping the source code. When
the script parsed the OG tags to HTML, it added a query string to all of the
URL's named "OSINTwProfile". As it is extremly unlikely that any website is
normally using this as a query string, it won't interact with the website, but
it is the easiest way of letting the second part of the script know which
article to look for the neccessary details in.

After locating the right profile for the article, the script uses the profile to
extract three categories of information from the article: 1. the small details
like the date, the author, the title and the subtitle, 2. the body of the
article including text, quotes, images and so on and 3. the text for the
article clear of any formatting, image or other things. The first two are
converted from HTML to markdown and the parsed directly to a markdown template,
in the same way the HTML was parsed to a template, but the cleartext for the article
undergoes a little processing first.

First the cleartext gets cleaned up a little bit by removing the html tags, weird
characthers that appear in text documents from the web along with a few other
properties that isn't desirable when processing text like words only consisting
of number or double space. After this it's compared to a 370.000 lines long
dictionary of commonly used english words, and all matches are removed from the
cleartext. After this the words are sorted by number of occurrences in the text,
and the ten most common words are added to the markdown file as tags. As these
aren't withing the 370.000 most used english words, they will often be technical
keywords that is relevant for the article, like names or specific technologies,
and while this form of tagging isn't perfect, it often gets the key points of
the article right.

After the new markdown file is then created, it's named after the title of the
article and moved to the obsidian vault. Obsidian is then openened in that
specific file using an URI scheme along with the "xdg-open" command for linux,
"start" command for windows, "cygstart" for a cygwin enviroment or the "open"
command for mac and the user is free to edit the file.

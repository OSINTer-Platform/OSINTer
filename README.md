![OSINTer](https://raw.githubusercontent.com/bertmad3400/OSINTer/master/logo.png)
# Introduction
OSINTer is an open source intelligence gathering tool, designed to ease the intelligence gathering process by scraping reliable intelligence news sources, and presenting them in an easy to navigate UI, to allow intelligence analysts to look at a great deal of intelligence collectively.
OSINTer is split into multiple repositories for ease of development.
| Repository | Description |
| --- | --- |
| ![OSINTansible](https://github.com/bertmad3400/OSINTansible) | Responsible for making the installation process easier, by using ansible. |
| ![OSINTbackend](https://github.com/bertmad3400/OSINTbackend) | Which is responsible for the scraping and initialization of OSINTer. |
| ![OSINTmodules](https://github.com/bertmad3400/OSINTmodules) | Which is responsible for handling many of the finer operations, such as the scraping, text handling, and DBMS. |
| ![OSINTprofiles](https://github.com/bertmad3400/OSINTmodules) | Which is responsible for specifying the various sources that are scraped for intelligence. |
| ![OSINTwebserver](https://github.com/bertmad3400/OSINTwebserver) | Which is responsible for displaying the intelligence in an easy to view format.|

## What problem does OSINTer solve?
The process of gathering cyber threat intelligence is only as successful as the investigators ability to identify relevant intelligence sources. Identifying relevant and reliable sources could often be a time-consuming task, as the CTI personnel would have to first locate the intelligence source, then read it to identify its relevance and usefulness as well as identify its formatting, and finally mark down all relevant details for usage in their report.<br>
This is time consuming and can be hit and miss depending on the skill and experience of the CTI personnel.

## How does OSINTer Solve the Problem?
Firstly, to combat the time-consuming task of identifying relevant threat intelligence sources, OSINTer gathers information from known, reliable sources, automatically, and then displays these in its webservice interface in a list sorted by publish date. Providing the most current information first, and in a consistent format so that users can easily identify the relevant information sources for their CTI reports.<br>
Secondly, the information is archived and the webservice provides functionality for users to download Obsidian Markdown files. These files, when imported into Obsidian, allows the user to analyze on all or parts of the collected information. Obsidian has tools to easily detect correlations between the information, providing a much-needed overview of the collected information. 

## How do we intend to use OSINTer?
Firstly, we intend to utilize this in our work with the CTI subscription service. With OSINTer deployed internally, the CTI team can easily identify relevant sources for the CTI reports.<br>
Secondly, the tool can later be used in integrations with detection tools to be made further down the line. This will allow to expand its usage inside future services Combitech may wish to provide, including Project Grapevine.


# Quickstart/How-To-Use
- Install the ansible package from your repos along with python 3 and the "cryptography" python package.
- Setup a new server using one of the supported distributions listed below and configure a regular user with sudo and SSH access using an SSH key.
  <br>While it is not neccessarily needed to install python 3 on the remote machine, it is recommended, to limit the possibilities of bugs.
- Clone the <a href="https://github.com/bertmad3400/OSINTansible">OSINTansible</a> git repo and navigate to that directory
- Execute ``` ansible-playbook -K playbooks/main.yml -u [regular_user] -i [remotes] --key-file [private_key_location] ``` with remotes being a comma seperated list of remote servers (add a single trailing comma if only using one remote server), regular_user being the regular, non-root user you set up just before and private_key_location being the path to the private key for your ssh connection.
- When using an SSH key, remember to protect it with ```chmod 400 [private_key_location]```.
- Supply the password for the [regular_user] when asked for the "BECOME password". This will be used for sudo priviledge escalation when needed.
- For distributions with a firewall pre-installed (CentOS and Rocky Linux) remember to open port 80 and 443 on the right interfaces to allow HTTPS and HTTP traffic comming in and out.


# Supported Systems
Currently, these are the supported distributions using x86_64 architecture:
- Debian 10/11
- Arch
- Ubuntu Server 20
- CentOS Linux 8
- Rocky Linux 8
<br>We do recommend running OSINTer on Arch Linux, as this has proven to have a substantial perfomance increase over the other distributions during our veryextensive testing, but we do realize that this unfortunatly isn't possible foreveryone, and therefore we fully support the other platforms listed.


# Technical
While OSINTer is designed to be installed on a host or series of hosts, which have just been installed, it can also be installed on host(s) running other software. Keep in mind that doing so will probably interfere with the following list of software if it's already installed:

## Nginx
OSINTer utilizes Nginx to utilize the frontend portion of the solution. In order to do so, the webserver will be reconfigured for OSINTer.
- It will replace the nginx config file found at /etc/nginx/nginx.conf◇ This will make the nginx service run as the osinter-web user
- It will create a new site in /etc/nginx/site-available and create a symlinkto that in /etc/nginx/sites-enabled
- It will restart the service

## PostgreSQL
In order to store the collected information, OSINTer utilizes PostgreSQL. If the server already has PostgreSQL installed it will be reconfigured for OSINTer:
- On non-Debian based systems, it will try to initialize a new DB cluster inthe default location.◇ For Arch this is var/lib/postgres/data as defined in the Archlinux.jsonfile and for CentOS/Rocky Linux this is /var/lib/pgsql/data as pre-definedby the OS
- It will replace the postgres.conf file and the pg_hba.conf file◇ This will keep the authenification method for the postgres user as beingpeer-authentification
   → This will prevent any kind of connection to the DB using anything elsebut the unix socket
- It will create a new DB and a whole range of new users described in thepg_hba.conf file
- It will restart the service

## Custom Certificates
When installing OSINTer you have the option of providing it with a CA certificate and CA private key, then the ansible installation will write a certificate for your server, which it will utilize for it's webfront. Alternatively OSINTer will generate a selfsigned certificate which will be used instead. The process of using your own CA is as follows:
- Rename a copy of the CA private key to "ca.key" and move it to the "./vars/CA"directory in the OSINTer-ansible folder before installing
- Rename a copy of a certificate signed by the CA to "ca.crt" and move it to that same directory
- Now simply follow the instructions in the quick guide to install OSINTer. The ansible playbooks will automatically recognize the CA and use it for signing the certificates.

## What are profiles?
To understand the script, an understanding of the profiles that enables this script to run in the first place is certainly neccessary. Profiles are in short simply data structured in a JSON format specifying where and what to scrape. These are custom created on a site to site basis, and since nearly all news sites have the same structure (more or less) on all of their articles, they're made to describe some generic rules on where to find given pieces of information on a page, like in what HTML element with what tag the date is to be found, or what element is encapsulating the text in the articles.

The goal with the profiles is to be as generic as possible, with the most in common with each other, to prevent a programming hell of having to program in every possible edge case that could appear in an article, and instead allow the script to use a few simple rules for scraping the articles that are the same for all sites. With that said though there are two different types of profiles, fortwo different kinds of websites. The first one is for the sites that offer are liable RSS feed which conform to standards. This one is the prefered method, since it's not only the simplest method for gathering the newest articles from asite, but oftentimes also the most reliable.

Some site hovewer, does not offer a RSS feed, or maybe they, but it doesn't conform to the standard. Here classic webscraping of the front page is used to find the 10 newest articles, and while it does not offer the same reliability as the RSS feeds, it does allow for gathering of articles from basically any news site.


## In Depth Details
So how does OSINTer function? There is a (admittedly quite primitive) flowchart included in this repo, but if that's not your coup of tea, then here a quick rundown of the inner functions of OSINTer.

First the script reads the profiles (which also acts as a list of news sites to scrape) and based on those scrapes the 10 most recent articles, either using static scraping of the front page or the RSS feed. The reason for only including the 10 most recent articles, is that a lot of news sites doesn't include more in their RSS feed or on their front page without any user interaction, and the limit is kept at 10 to prevent excesive programming of edge cases and worst case a severe overweight of some sites.

After this the OG (Open Graph) tags for each article is scraped. These are the title, a description along with an image and the source url for the article are used a little later, for creating a front end using HTML, CSS and JavaScript for letting the user choose an article to read. This proccess is done in parallel for each news site, to prevent it from becoming too slow when adding more profiles.

As stated, these OG tags are then formatet into HTML (and CSS) and injected into two templates, one for the HTML/CSS and one for the JavaScript, and the newly created HTML file is rendered in a firefox browser driven by the geckodriver using the selenium framework. The reason for using the OG tags for presenting the articles, is that they're designed to give a short introduction to what the article contains, which is fitting for this usecase.

By clicking one of the articles presentet visually, the user will then be taken to the article of their choice, and while the user is reading the article, the script is collecting the source code of the article a long with the url for it in the background for later use. The pros of using the same browser for scraping and presenting the article to the user - outside of not having to request the same webpage twice - is that the script will get the excact code that is seen visually by the user. This means that even if the article has some dynamic loading, or possibly a "Read more" button, that would normally come in the way of normal static webscraping - or sometimes even dynamic scraping - it will not have an influence here, since everything the user reads will be visible to the script.

When the user then closes the article, the script gathers the source code for the article (since this is then the "final" version of the article) along with the URL for the article. The URL itself is used for two things; First of all simply for providing a source for the article when parsing it to markdown, but two; also for specifying which profile to use for scraping the source code. When the script parsed the OG tags to HTML, it added a query string to all of the URL's named "OSINTerProfile". As it is extremly unlikely that any website is normally using this as a query string, it won't interact with the website, but it is the easiest way of letting the second part of the script know which article to look for the neccessary details in.

After locating the right profile for the article, the script uses the profile to extract three categories of information from the article: 1. the small details like the date, the author, the title and the subtitle, 2. the body of the article including text, quotes, images and so on and 3. the text for the article clear of any formatting, image or other things. The first two are converted from HTML to markdown and the parsed directly to a markdown template, in the same way the HTML was parsed to a template, but the cleartext for the article undergoes a little processing first.

First the cleartext gets cleaned up a little bit by removing the html tags, weird characthers that appear in text documents from the web along with a few other properties that isn't desirable when processing text like words only consisting of number or double space. After this it's compared to a 370.000 lines long dictionary of commonly used english words, and all matches are removed from the cleartext. After this the words are sorted by number of occurrences in the text, and the ten most common words are added to the markdown file as tags. As these aren't withing the 370.000 most used english words, they will often be technical keywords that is relevant for the article, like names or specific technologies, and while this form of tagging isn't perfect, it often gets the key points of the article right.

After the new markdown file is then created, it's named after the title of the article and moved to the obsidian vault. Obsidian is then openened in that specific file using an URI scheme along with the "xdg-open" command for linux, "start" command for windows, "cygstart" for a cygwin enviroment or the "open" command for mac and the user is free to edit the file.


# Contributers
## People
Thanks to all of these people for assisting in making this project become a reality.<br>
<a href="https://github.com/bertmad3400/"><img src="https://avatars.githubusercontent.com/u/57845632?v=4" width="50" height="50" alt="Bertmad3400"/></a>
<a href="https://github.com/TheHangryBadger/"><img src="https://avatars.githubusercontent.com/u/74346591?v=4" width="50" height="50" alt="TheHangryBadger"/></a>
<a href="https://github.com/dtclayton/"><img src="https://avatars.githubusercontent.com/u/46198611?v=4" width="50" height="50" alt="dtclayton"/></a>

## Organisations
Thanks to <b>Combitech A/S</b> for helping with kickstarting the idea and allocating resources for the project development.<br>
<a href="https://www.combitech.com/denmark"><img src="https://www.combitech.com/siteassets/combitech-logo-vitbg.png"/></a>

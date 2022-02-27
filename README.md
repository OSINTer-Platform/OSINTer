# OSINTer
[![OSINTer](https://raw.githubusercontent.com/bertmad3400/OSINTer/master/logo.png)](https://osinter.dk)

## *Looking for help*
OSINTer has grown a lot the last few months, and after adopting a new backend powered by Elasticsearch, it has become able to handle very large amounts of data. Therefore we are currently looking into machine learning for doing a bit of data analysis (specifically text summarization and data clustering), but unfortunately my knowledge on the subject is rather sparse. Therefore, if you're data scientist/analysis, or programmer who has a hold these subjects, and would like to contribute to OSINTer, please reach out on skrivtilbertram@gmail.com. As the project is free and open-source (and I'm doing the development unpaid) I unfortunately do not have the possibility of paying for your work, but at least there's plenty of currated real-world data and interresting challenges.

## Introduction
OSINTer is an open source intelligence gathering tool, designed to ease the intelligence gathering process by scraping reliable intelligence news sources, and presenting them in an easy to navigate UI, hosted as a webserver, to allow intelligence analysts to look at a great deal of intelligence collectively.

OSINTer is split into multiple repositories for ease of development, listed below:
| Repository | Description |
| --- | --- |
| ![OSINTansible](https://github.com/bertmad3400/OSINTansible) | Responsible for making the installation process easier, by using ansible. |
| ![OSINTbackend](https://github.com/bertmad3400/OSINTbackend) | Responsible for the scraping and initialization of OSINTer. |
| ![OSINTmodules](https://github.com/bertmad3400/OSINTmodules) | Responsible for handling many of the finer operations, such as the scraping, text handling, and DBMS. |
| ![OSINTprofiles](https://github.com/bertmad3400/OSINTprofiles) | Responsible for specifying the various sources that are scraped for intelligence. |
| ![OSINTwebserver](https://github.com/bertmad3400/OSINTwebserver) | Responsible for displaying the intelligence in an easy to view format.|

 For a demonstration of how it looks and works, have a look at our demo-site at [OSINTer.dk](https://osinter.dk)

## What problem does OSINTer attempt to solve?
The process of gathering cyber threat intelligence is only as successful as the investigators ability to identify relevant intelligence sources. Identifying relevant and reliable sources could often be a time-consuming task, as the CTI personnel would have to first locate the intelligence source, then read it to identify its relevance and usefulness as well as identify its formatting, and finally mark down all relevant details for usage in their report. This is time consuming and can be hit and miss depending on the skill and experience of the CTI personnel, and while products to combat this repetitive and time-consuming task, like Recorded Future, exists, these are often not only expensive, but also closed in nature, as they rarely integrate well with thirdparty utilities.

The goal of OSINTer is to build an open-source and extensible platform for collecting and organizing open-source intelligence in a way that easily intergrates with thirdparty utilities and other pieces of open-source software. As such, it never was (and never will be) intended to compete with products like the aforementioned Recorded Future, since the core concept is very different and since OSINTer does not offer the needed analysis capabilities on its own.


## How does OSINTer Solve the Problem?
Firstly, to combat the time-consuming task of identifying relevant threat intelligence sources, OSINTer gathers information from known, reliable sources, automatically, and then displays these in its webservice interface in a list sorted by publish date. This provides the most current information first, and in a consistent format so that users can easily identify the relevant information sources for their CTI reports or other use cases.

Secondly, the content from the threat intelligence sources is archived and retrievable for the user, through a download functionality in OSINTer, which allows for download Markdown files containing this content, and formattet in a consisten fashion. These files, when imported into any markdown editor (preferably Obsidian), allows the user to analyze on all or parts of the collected information. Obsidian has tools to easily detect correlations between the information, providing a much-needed overview of the collected information.

## How do we intend to use OSINTer?
Our current intent with OSINTer is deploying it internally where needed as to aid CTI team in easily identify relevant sources for future CTI reports, and to deploy a single central instance of OSINTer to start building an archive of historical data.

In the future, it is hovewer also our intend to use OSINTer in conjunction with detection and analysis tools made further down the line. There is currently an effort ongoing to convert the backend of OSINTer from a RDBMS and files on the disk, to an Elasticsearch cluster, which would not only allow extensibility in a way that is currently impossible, potentially allowing for intercommunication between OSINTer instances, and allow for integration of future tools, like Project Grapevine plan proposed by Combitech.


# Quickstart/How-To-Use
- Install the ansible package from your repos along with python 3 and the "cryptography" python package.
- Setup a new server using one of the supported distributions listed below and configure a regular user with sudo and SSH access using an SSH key.
  While it is not neccessarily needed to install python 3 on the remote machine, it is recommended, to limit the possibilities of bugs.
- Clone the <a href="https://github.com/bertmad3400/OSINTansible">OSINTansible</a> git repo and navigate to that directory
- Execute ``` ansible-playbook -K playbooks/main.yml -u [regular_user] -i [remotes] --key-file [private_key_location] ``` with remotes being a comma seperated list of remote servers (add a single trailing comma if only using one remote server), regular_user being the regular, non-root user you set up just before and private_key_location being the path to the private key for your ssh connection.
- When using an SSH key, remember to protect it with ```chmod 400 [private_key_location]```.
- Supply the password for the [regular_user] when asked for the "BECOME password". This will be used for sudo priviledge escalation when needed.
- For distributions with a firewall pre-installed (CentOS and Rocky Linux) remember to open port 80 and 443 on the right interfaces to allow HTTPS and HTTP traffic comming in and out.

## Potential problems
While OSINTer is designed to be installed on a host or series of hosts, which have just been installed, it can also be installed on host(s) running other software. Keep in mind that doing so will probably interfere with the following list of software if it's already installed:

### Nginx
OSINTer utilizes Nginx to utilize the frontend portion of the solution. In order to do so, the webserver will be reconfigured for OSINTer.
- It will replace the nginx config file found at /etc/nginx/nginx.conf◇ This will make the nginx service run as the osinter-web user
- It will create a new site in /etc/nginx/site-available and create a symlinkto that in /etc/nginx/sites-enabled
- It will restart the service

# Supported Systems
Currently, these are the supported distributions using x86_64 architecture:
- Debian 10/11
- Arch
- Ubuntu Server 20
- CentOS Linux 8
- Rocky Linux 8

# Custom Certificates for the frontend
When installing OSINTer you have the option of providing it with a CA certificate and CA private key, then the ansible installation will write a certificate for your server, which it will utilize for it's webfront. Alternatively OSINTer will generate a selfsigned certificate which will be used instead. The process of using your own CA is as follows:
- Rename a copy of the CA private key to "ca.key" and move it to the "./vars/CA"directory in the OSINTer-ansible folder before installing
- Rename a copy of a certificate signed by the CA to "ca.crt" and move it to that same directory
- Now simply follow the instructions in the quick guide to install OSINTer. The ansible playbooks will automatically recognize the CA and use it for signing the certificates.

# Kibana Dashboards
As OSINTer uses Elasticsearch in the backend for storing data, Kibana can be used to visualize the information scraped by OSINTer. To simplify this proccess, this repo includes a couple of Kibana Dashboards in the KibanaDashboards directory, which (if Kibana has been setup and connected to the same Elasticsearch as OSINTer) can be imported into Kibana using the following command:

``` curl -X POST "[kibana_web_adress]/api/saved_objects/_import?createNewCopies=true" -H "kbn-xsrf: true" --form file=@[dasboard_file_name] ```

Example of how to use command, with Kibana running on localhost, with an elastic user with the password set to "elastic" and using the Articles dashboard:

``` curl -X POST "https://elastic:elastic@localhost:5601/api/saved_objects/_import?createNewCopies=true" -H "kbn-xsrf: true" --form file=@./KibanaDashboards/OSINTerArticles.ndjson```



# Contributers
## People
Thanks to all of these people for assisting in making this project become a reality.<br>
<a href="https://github.com/bertmad3400/"><img src="https://avatars.githubusercontent.com/u/57845632?v=4" width="100" height="100" alt="bertmad3400"/></a>
<a href="https://github.com/TheHangryBadger/"><img src="https://avatars.githubusercontent.com/u/74346591?v=4" width="100" height="100" alt="TheHangryBadger"/></a>
<a href="https://github.com/dtclayton/"><img src="https://avatars.githubusercontent.com/u/46198611?v=4" width="100" height="100" alt="dtclayton"/></a>

## Organisations
Thanks to Combitech A/S for helping with kickstarting the idea and allocating resources for the project development.

<a href="https://www.combitech.com/denmark"><img src="https://www.combitech.com/siteassets/combitech-logo-vitbg.png" width="400"/></a>

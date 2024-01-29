# OSINTer
[![OSINTer](https://raw.githubusercontent.com/OSINTer-Platform/OSINTer/master/logo/full.png)](https://osinter.dk)

## Contributing
As OSINTer is open-source we highly encourage
any form of contributing. Should you want to contribute, then please get involved with this GitHub, og get in
contact either at contact@osinter.dk or on the Github repos (if you are reading
this on Gitlab, then that is simply a downstream mirror).

## Introduction
OSINTer is a - previously open-source, now just source-available - intelligence
gathering tool, designed to ease the intelligence gathering process by scraping
reliable intelligence news sources, and presenting them in an easy to navigate
UI, hosted as a web-application, to allow intelligence analysts to handle large
amounts of intelligence.

OSINTer is split into multiple repositories for ease of development, listed
below:
| Repository | Description |
| --- | --- |
| [OSINTansible](https://github.com/OSINTer-platform/ansible) | Responsible for making the installation process easier, by using ansible. |
| [OSINTbackend](https://github.com/OSINTer-platform/backend) | Responsible for the scraping and initialization of OSINTer. |
| [OSINTmodules](https://github.com/OSINTer-platform/modules) | Responsible for cross-repo functionality. |
| [OSINTapi](https://github.com/OSINTer-platform/api) | Responsible for displaying the intelligence in an easy to view format.|
| [OSINTwebfrontend](https://github.com/OSINTer-platform/webfrontend2) | Responsible for displaying the intelligence in an easy to view format.|
| [OSINTprofiles](https://github.com/OSINTer-platform/profiles) | Responsible for specifying the various sources that are scraped for intelligence. |
| [OSINTblog](https://github.com/OSINTer-platform/blog) | Responsible for the content at the blog associated with OSINTer |


 For a demonstration of how it looks and works, have a look at our demo-site at
 [OSINTer.dk](https://osinter.dk)

## What problem does OSINTer attempt to solve?
The process of gathering cyber threat intelligence is only as successful as the
investigators ability to identify relevant intelligence sources. Identifying
relevant and reliable sources could often be a time-consuming task, as the CTI
personnel would have to first locate the intelligence source, then read it to
identify its relevance and usefulness as well as identify its formatting, and
finally mark down all relevant details for usage in their report. This is time
consuming and can be hit and miss depending on the skill and experience of the
CTI personnel, and while products to combat this repetitive and time-consuming
task, like Recorded Future, exists, these are often not only expensive, but
also closed in nature, as they rarely integrate well with third-party
utilities.

The goal of OSINTer is to build an open-source and extensible platform for
collecting and organizing open-source intelligence in a way that easily
integrates with third-party utilities and other pieces of open-source software.
As such, it never was (and never will be) intended to compete with products
like the aforementioned Recorded Future, since the core concept is very
different and since OSINTer does not offer the needed analysis capabilities on
its own.


## How does OSINTer Solve the Problem?
Firstly, to combat the time-consuming task of identifying relevant threat
intelligence sources, OSINTer gathers information from known, reliable sources,
automatically, and then displays these in its web-interface in a list sorted by
publish date. This provides the most current information first, and in a
consistent format so that users can easily identify the relevant information
sources for their CTI reports or other use cases.

Secondly, the content from the threat intelligence sources is archived and
retrievable for the user, through a download functionality in OSINTer, which
allows for download Markdown files containing this content, and formatted in a
consistent fashion. These files, when imported into any markdown editor
(preferably Obsidian), allows the user to analyze on all or parts of the
collected information. Obsidian has tools to easily detect correlations between
the information, providing a much-needed overview of the collected information.

## How do we intend to use OSINTer?
Our current intent with OSINTer is deploying it internally where needed as to
aid CTI team in easily identify relevant sources for future CTI reports, and to
deploy a single central instance of OSINTer to start building an archive of
historical data.

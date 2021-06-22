{
  "source": {
    "name": "ZDNet",
    "profileName": "zdnet",
    "address": "https://www.zdnet.com/",
    "retrivalMethod": "scraping",
    "newsPath": "https://www.zdnet.com/topic/security/",
    "scrapingTargets": {
      "linkClass": "",
      "element": "article",
      "class": "item"
    }
  },
  "scraping": {
    "type": "static",
    "details": {
      "title": {
        "containerClass": "storyHeader article",
        "element": "h1",
        "class": ""
      },
      "subtitle": {
        "containerClass": "storyHeader article",
        "element": "p",
        "class": "summary"
      },
      "date": {
        "containerClass": "meta",
        "element": "time",
        "class": ""
      },
      "author": {
        "containerClass": "meta",
        "element": "span",
        "class": ""
      }
    },
    "content": {
      "containerClass": "storyBody",
      "element": "p;h3;blockquote;img",
      "class": "",
	  "remove": ""
    }
  }
}

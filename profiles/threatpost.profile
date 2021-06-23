{
  "source": {
    "name": "ThreatPost",
    "profileName": "threatpost",
    "address": "https://threatpost.com/",
    "retrivalMethod": "rss",
    "newsPath": "https://threatpost.com/feed"
  },
  "scraping": {
    "type": "static",
    "details": {
      "title": {
        "containerClass": "c-article__header",
        "element": "h1",
        "class": "c-article__title"
      },
      "subtitle": {
        "containerClass": "c-article__intro",
        "element": "p",
        "class": ""
      },
      "date": {
        "containerClass": "c-article__time",
        "element": "time",
        "class": ""
      },
      "author": {
        "containerClass": "c-article__author",
        "element": "a",
        "class": "c-article__author-name"
      }
    },
    "content": {
      "containerClass": "c-article__main",
      "element": "p;h2;img;blockquote",
      "class": "",
	  "remove": "img,wp-image-141989",
	  "recursive": "False"
    }
  }
}

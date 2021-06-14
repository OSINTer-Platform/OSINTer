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
      "subtitle": "",
      "date": {
        "containerClass": "c-article__time",
        "element": "time",
        "class": ""
      },
      "author": {
        "containerClass": "c-article__author",
        "element": "span",
        "class": ""
      }
    },
    "content": {
      "containerClass": "c-article__main",
      "element": "p;h2;img;blockquote",
      "class": ""
    }
  }
}

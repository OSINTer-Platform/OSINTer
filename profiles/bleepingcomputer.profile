{
  "source": {
    "name": "Bleeping Computer",
    "profileName": "bleepingcomputer",
    "address": "https://www.bleepingcomputer.com/",
    "retrivalMethod": "rss",
    "newsPath": "https://www.bleepingcomputer.com/feed/"
  },
  "scraping": {
    "type": "no-action",
    "details": {
      "title": {
        "containerClass": "article_section",
        "element": "h1",
        "class": ""
      },
      "subtitle": "",
      "date": {
        "containerClass": "cz-news-title-right-area",
        "element": "li",
        "class": "cz-news-date"
      },
      "author": {
        "containerClass": "author",
        "element": "span",
        "class": ""
      }
    },
    "content": {
      "containerClass": "articleBody",
      "element": "p;h2;h3;img;blockquote;a;ul;li;ol;div;figure",
      "class": "",
      "headerImage": "",
      "remove": "cnx,cnx-main-container cnx-in-desktop cnx-ps cnx-main-container-flex",
      "recursive": "False"
    }
  }
}

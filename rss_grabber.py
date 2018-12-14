import sys
from urllib.parse import urlparse

import feedparser
import justext
import requests


RSS_FEEDS_SOURCE = 'rss_feeds.txt'


class Feed:
    url = ''

    def __init__(self):
        self._feed_entries = feedparser.parse(self.url)['entries']

    def news(self, limit=None):
        oldkey, newkey = 'summary', 'desc'
        news = [
            {
                newkey if k == oldkey else k: v
                for k, v in d.items()
                if k in ('title', 'link', 'summary', 'published')
            }
            for d in self._feed_entries[:limit]
        ]

        return news

    def grub(self, link):
        article_content = {}
        feed_entry = next(
            entry for entry in self._feed_entries
            if entry.link == link
        )
        article_content['title'] = feed_entry.title
        for entry in feed_entry.links:
            if entry.get('type', None).startswith('image'):
                article_content['image'] = entry.href
            else:
                article_content['image'] = ''

        page = requests.get(link)
        language = justext.get_stoplist("Russian")
        justext_objects = justext.justext(page.content, language)
        paragraphs = [
            paragraph
            for paragraph in justext_objects
            if not paragraph.is_boilerplate
        ]
        article_content['content'] = paragraphs

        return article_content


def load_feeds(filename):
    with open(filename, 'r') as fp:
        while True:
            line = fp.readline().strip()

            if not line:
                break
            else:
                yield line


def extract_tld(url):
    return urlparse(url).netloc.split('.')[-2]


rss_feeds_url = load_feeds(RSS_FEEDS_SOURCE)

subclasses_names = [
    (extract_tld(url).capitalize(), url)
    for url in rss_feeds_url
]

for name, rss_url in subclasses_names:
    Class = type(name, (Feed,), {'url': rss_url})
    setattr(sys.modules[__name__], name, Class)

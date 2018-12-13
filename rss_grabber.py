import sys
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import feedparser
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
        soup = BeautifulSoup(page.content, 'lxml')
        paragraphs = [
            para.text
            for para in soup.find_all('p')
            if para.text != ''
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

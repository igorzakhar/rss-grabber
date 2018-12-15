import sys
import time
from urllib.parse import urlparse

from goose3 import Goose
import feedparser


RSS_FEEDS_SOURCE = 'rss_feeds.txt'
GOOSE_CONFIG = {
    'use_meta_language': False,
    'target_language': 'ru',
    'enable_image_fetching': True
}


class Feed:
    url = ''

    def __init__(self):
        self._feed_entries = feedparser.parse(self.url)['entries']
        self._extractor = Goose(GOOSE_CONFIG)

    def news(self, limit=None):
        oldkey, newkey = 'summary', 'desc'
        news = [
            {
                (newkey if key == oldkey else key) or
                key: (
                    time.strftime('%d.%m.%Y %H:%M', entry['published_parsed'])
                    if key == 'published' else value
                )
                for key, value in entry.items()
                if key in ('title', 'link', 'summary', 'published')
            }
            for entry in self._feed_entries
        ]
        return news

    def grub(self, link):
        article_content = {}
        article = self._extractor.extract(url=link)
        article_content['title'] = article.title

        if article.top_image:
            article_content['image'] = article.top_image.src
        else:
            article_content['image'] = ''

        article_content['content'] = article.cleaned_text.split('\n\n')

        return article_content


def extract_2level_domain(url):
    return urlparse(url).netloc.split('.')[-2]


def load_feeds(filename):
    with open(filename, 'r') as fp:
        while True:
            line = fp.readline().strip()

            if not line:
                break
            else:
                yield line


rss_feeds_url = load_feeds(RSS_FEEDS_SOURCE)

subclasses_names = [
    (extract_2level_domain(url).capitalize(), url)
    for url in rss_feeds_url
]

for name, rss_url in subclasses_names:
    Class = type(name, (Feed,), {'url': rss_url})
    setattr(sys.modules[__name__], name, Class)

import sys
from datetime import datetime
from urllib.parse import urlparse

from goose3 import Goose
import feedparser


GOOSE_CONFIG = {
    'use_meta_language': False,
    'target_language': 'ru',
    'enable_image_fetching': True
}


class Feed:
    url = ''

    def _get_feed_entries(self):
        feed = feedparser.parse(self.url)
        entries = feed.get('entries')
        return entries

    def _extract_article(self, link):
        article_extractor = Goose(GOOSE_CONFIG)
        article = article_extractor.extract(url=link)
        return article

    def news(self, limit=None):
        oldkey, newkey = 'summary', 'desc'
        news = [
            {
                (newkey if key == oldkey else key) or
                key: (
                    datetime.strptime(
                        entry['published'], '%a, %d %b %Y %H:%M:%S %z'
                    ).strftime(
                        '%d.%m.%Y %H:%M'
                    )
                    if key == 'published' else value
                )
                for key, value in entry.items()
                if key in ('title', 'link', 'summary', 'published')
            }
            for entry in self._get_feed_entries()[:limit]
        ]
        return news

    def grub(self, link):
        article_content = {}
        article = self._extract_article(link)
        article_content['title'] = article.title

        if article.top_image:
            article_content['image'] = article.top_image.src
        else:
            article_content['image'] = ''

        article_content['content'] = article.cleaned_text.split('\n\n')

        return article_content


def extract_2level_domain(url):
    return urlparse(url).netloc.split('.')[-2]


def load_urls_feeds(filename):
    with open(filename, 'r') as fp:
        while True:
            line = fp.readline().strip()

            if not line:
                break
            else:
                yield line


def add_feed(rss_url, name=''):
    if name == '':
        name = extract_2level_domain(rss_url).capitalize()
    Class = type(name, (Feed,), {'url': rss_url})
    setattr(sys.modules['__main__'], name, Class)
    return Class


def load_feeds_from_file(filename):
    try:
        rss_feeds_url = load_urls_feeds(filename)
        subclasses_names = [
            (extract_2level_domain(url).capitalize(), url)
            for url in rss_feeds_url
        ]
        for name, rss_url in subclasses_names:
            Class = type(name, (Feed,), {'url': rss_url})
            setattr(sys.modules['__main__'], name, Class)
    except OSError as error:
        raise error

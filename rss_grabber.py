import sys

import tldextract
import feedparser


RSS_FEEDS_SOURCE = 'rss_feeds.txt'


class Feed:
    url = ''
    _keys_entry = ('title', 'link', 'summary', 'published')

    def news(self, limit=None):
        feed_entries = feedparser.parse(self.url)['entries'][:limit]
        news = [
            {k: v for k, v in d.items() if k in self._keys_entry}
            for d in feed_entries
        ]

        return news

    def grub(self):
        pass


def load_feeds(filename):
    with open(filename, 'r') as fp:
        while True:
            line = fp.readline().strip()

            if not line:
                break
            else:
                yield line


thismodule = sys.modules[__name__]

rss_feeds_url = load_feeds(RSS_FEEDS_SOURCE)

subclasses_name = [
    (tldextract.extract(url).domain.capitalize(), url)
    for url in rss_feeds_url
]

for name, rss_url in subclasses_name:
    setattr(thismodule, name, type(name, (Feed,), {'url': rss_url}))

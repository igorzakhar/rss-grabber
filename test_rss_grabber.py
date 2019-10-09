import json
from unittest.mock import patch
import pytest

import rss_grabber


def feed_entries():
    with open('test_data/feedparser_response.json', 'r') as fp:
        test_feed = json.load(fp)
    return test_feed


@pytest.fixture()
def expected_news():
    with open('test_data/expected_data.json', 'r') as fp:
        expected_news = json.load(fp)
    return expected_news


@patch('rss_grabber.Feed._get_feed_entries', side_effect=feed_entries)
def test_get_news(MockedFeed, expected_news):
    feed = rss_grabber.Feed()
    news = feed.news()
    assert news == expected_news


@pytest.mark.parametrize('limit', [i for i in range(len(feed_entries())+1)])
@patch('rss_grabber.Feed._get_feed_entries', side_effect=feed_entries)
def test_news_limit(MockedFeed, limit):
    feed = rss_grabber.Feed()
    news = feed.news(limit=limit)
    assert len(news) == limit

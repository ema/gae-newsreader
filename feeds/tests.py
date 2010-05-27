from feeds.models import Feed

from feeds.models import insert_feed, insert_basic_feeds
from feeds.models import insert_users_and_subscriptions
from feeds.models import get_user_feeds

from django.test import Client

import unittest

class TestModels(unittest.TestCase):

    def tearDown(self):
        for el in Feed.all():
            el.delete()

    def test_create_feed(self):
        self.assertEquals(0, Feed.all().count())
        insert_feed('Slashdot', 'http://rss.slashdot.org/Slashdot/slashdot',
            'News for nerds')
        self.assertEquals(1, Feed.all().count())

    def test_insert_basic(self):
        self.assertEquals(0, Feed.all().count())
        insert_basic_feeds()
        self.failUnless(Feed.all().count() > 1)

    def test_get_user_feeds(self):
        insert_basic_feeds()
        insert_users_and_subscriptions()
        
        self.assertEquals(2, len(get_user_feeds('ema')))
        self.assertEquals(1, len(get_user_feeds('foo')))
        self.assertEquals(0, len(get_user_feeds('does-not-exist')))

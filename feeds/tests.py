from feeds.models import Feed

from feeds.models import add_feed
from feeds.models import insert_users_and_subscriptions
from feeds.models import get_user_feeds, get_feed

from django.test import Client

import unittest

class TestModels(unittest.TestCase):

    def tearDown(self):
        for el in Feed.all():
            el.delete()

    def test_create_feed(self):
        self.assertEquals(0, Feed.all().count())
        add_feed('http://rss.slashdot.org/Slashdot/slashdot')
        self.assertEquals(1, Feed.all().count())

    def test_get_user_feeds(self):
        insert_users_and_subscriptions()
        
        self.assertEquals(0, len(get_user_feeds('does-not-exist')))
        self.assertEquals(1, len(get_user_feeds('foo')))
        self.failUnless(len(get_user_feeds('ema')))

    def test_get_feed(self):
        for feed in Feed.all():
            self.failUnless(get_feed(str(feed.key())))

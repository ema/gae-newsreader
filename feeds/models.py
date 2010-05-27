from appengine_django.models import BaseModel
from google.appengine.ext import db

import feedparser
import logging

class Feed(BaseModel):
    name = db.StringProperty(required=True)
    url = db.LinkProperty(required=True)
    description = db.StringProperty()

class User(BaseModel):
    name = db.StringProperty(required=True)

class Subscription(BaseModel):
    user = db.ReferenceProperty(User) 
    feed = db.ReferenceProperty(Feed)


def get_user(username):
    try:
        user = User.all().filter('name', username)[0]
        return user
    except IndexError:
        return None

def get_user_feeds(username):
    user = get_user(username)

    if user is None:
        return []

    return [ sub.feed for sub in Subscription.all().filter('user', user) ]

def get_feed(feed_key):
    """Feed with the given feed_key (str)

    get_feed(feed_key) -> Feed"""
    return db.get(db.Key(feed_key))

def add_feed(rssurl):
    channels = feedparser.parse(rssurl)

    feed = Feed(name=channels['feed']['title'], url=rssurl,
        description=channels['feed']['subtitle'])

    feed.put()
    return feed

def add_user_subscription(username, rssurl):
    user = get_user(username)
    assert user is not None

    feed = Feed.all().filter('url', rssurl)

    if feed.count() == 0:
        logging.info("adding, feed not found in datastore: %s" % rssurl)
        feed = add_feed(rssurl)
    else:
        logging.info("not adding, feed already in datastore: %s" % rssurl)
        feed = feed[0]

    subscription = Subscription(user=user.key(), feed=feed.key())

    return subscription.put()

# XXX
BASIC_FEEDS = (
    'http://rss.slashdot.org/Slashdot/slashdot',
    'http://rss.cnn.com/rss/edition.rss',
    'http://www.repubblica.it/rss/homepage/rss2.0.xml',
    'http://feeds.arstechnica.com/arstechnica/index/',
    'http://www.elpais.com/rss/feed.html?feedId=1022',
)

def insert_users_and_subscriptions():
    user = User(name="ema")
    user.put()

    for feed in BASIC_FEEDS:
        add_user_subscription(user.name, feed)

    user = User(name="foo")
    user.put()
    feed = BASIC_FEEDS[2]
    add_user_subscription(user.name, feed)

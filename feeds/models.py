from appengine_django.models import BaseModel
from google.appengine.ext import db

class Feed(BaseModel):
    name = db.StringProperty(required=True)
    url = db.LinkProperty(required=True)
    description = db.StringProperty()

class User(BaseModel):
    name = db.StringProperty(required=True)

class Subscription(BaseModel):
    user = db.ReferenceProperty(User) 
    feed = db.ReferenceProperty(Feed)

def insert_feed(name, url, description):
    feed = Feed(name=name, url=db.Link(url), description=description)
    return feed.put()

def insert_basic_feeds():
    feeds = [ 
        ( 'Slashdot', 'http://rss.slashdot.org/Slashdot/slashdot', 'News for nerds' ),
        ( 'CNN', 'http://rss.cnn.com/rss/edition.rss', 'CNN' ),
        ( 'Repubblica', 'http://www.repubblica.it/rss/homepage/rss2.0.xml', 'Repubblica.it' ),
    ]

    for feed in feeds:
        insert_feed(feed[0], feed[1], feed[2])

def insert_users_and_subscriptions():
    user = User(name="ema")
    user.put()
    
    feeds = Feed.all()

    for feed in feeds[:2]:
        subscription = Subscription(user=user.key(), feed=feed.key())
        subscription.put()

    user = User(name="foo")
    user.put()
    feed = feeds[2]
    subscription = Subscription(user=user.key(), feed=feed.key())
    subscription.put()

def get_user_feeds(username):
    try:
        user = User.all().filter('name', username)[0]
    except IndexError:
        return []

    return [ sub.feed for sub in Subscription.all().filter('user', user) ]

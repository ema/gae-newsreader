from models import User
from feeds.models import insert_users_and_subscriptions, insert_basic_feeds

if User.all().count() == 0:
    insert_basic_feeds()
    insert_users_and_subscriptions()

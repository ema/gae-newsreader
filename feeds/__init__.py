from models import User
from feeds.models import insert_users_and_subscriptions

if User.all().count() == 0:
    insert_users_and_subscriptions()

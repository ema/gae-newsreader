
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404

from feeds.models import get_user, get_user_feeds, get_feed, get_users
from feeds.models import add_user_subscription
from feeds.models import User

import feedparser

import logging

from google.appengine.api import users

def auth_decorator(function):
    def new_view(*args, **kwargs):
        request = args[0]

        user = users.get_current_user()

        if user:
            kwargs['logout_url'] = users.create_logout_url(request.META['PATH_INFO'])
            kwargs['user'] = user
        else:
            kwargs['login_url'] = users.create_login_url(request.META['PATH_INFO'])

        return function(*args, **kwargs)

    return new_view

def username_nickname_match(function):
    def new_view(*args, **kwargs):
        username = kwargs['username']

        user = users.get_current_user()
        if user and user.nickname() == username:
            return function(*args, **kwargs)

        return HttpResponse("", status=401)

    return new_view

@auth_decorator
def user_feeds(request, username, logout_url=None, login_url=None, user=None):
    # let's add this user if logged in and not present in db
    db_user = get_user(username)

    if user and not db_user and username == user.nickname():
        db_user = User(name=user.nickname())
        db_user.put()

    logging.info("%s - %s" % (username, user))
    logging.info(str(db_user))

    if db_user:
        user_feeds = get_user_feeds(username)
        return render_to_response("list_feeds.html", locals())

    raise Http404

@auth_decorator
def render_feed(request, username, feed_key, logout_url=None, login_url=None,
        user=None):

    feed = get_feed(feed_key)

    entries = []
    channels = feedparser.parse(feed.url)
    for entry in channels.entries:
        entries.append(dict(title=entry.title,
            description=entry.description, link=entry.link))

    return render_to_response("render_feed.html", locals())

@username_nickname_match
def add_feed(request, username):
    rssurl = request.POST['rssurl']

    try:
        add_user_subscription(username, rssurl)
    except KeyError:
        return HttpResponse("Cannot parse feed: %s" % rssurl)

    return HttpResponseRedirect('/%s/' % username)

@auth_decorator
def homepage(request, logout_url=None, login_url=None, user=None):
    users_list = [ u for u in get_users() if get_user_feeds(u.name) ]
    return render_to_response("homepage.html", locals())

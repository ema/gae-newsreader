
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404

from feeds.models import get_user, get_user_feeds, get_feed
from feeds.models import add_user_subscription

import feedparser

import logging

def user_feeds(request, username):
    logging.info("user_feeds(%s)" % username)

    if not get_user(username):
        return Http404()

    user_feeds = get_user_feeds(username)
    return render_to_response("list_feeds.html", locals())

def render_feed(request, username, feed_key):
    feed = get_feed(feed_key)

    entries = []
    channels = feedparser.parse(feed.url)
    for entry in channels.entries:
        entries.append(dict(title=entry.title,
            description=entry.description, link=entry.link))

    return render_to_response("render_feed.html", locals())

def add_feed(request, username):
    rssurl = request.POST['rssurl']

    try:
        add_user_subscription(username, rssurl)
    except KeyError:
        return HttpResponse("Cannot parse feed: %s" % rssurl)

    return HttpResponseRedirect('/%s/' % username)

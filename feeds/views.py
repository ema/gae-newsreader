
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404

from feeds.models import get_user, get_user_feeds, get_feed

import logging

def user_feeds(self, username):
    logging.info("user_feeds(%s)" % username)

    if not get_user(username):
        return Http404()

    user_feeds = get_user_feeds(username)
    return render_to_response("list_feeds.html", locals())

def render_feed(self, username, feed_key):
    feed = get_feed(feed_key)
    return render_to_response("render_feed.html", locals())

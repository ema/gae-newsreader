"""
Find RSS feeds for the given keyword parsing HTML documents returned by Google
search results.
"""
import urllib2
import simplejson
from BeautifulSoup import BeautifulSoup, SoupStrainer

import unittest

SEARCH_API = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s"

def google_search(keyword):
    """Google results for the given search term"""
    keyword = urllib2.quote(keyword)

    url = SEARCH_API % keyword

    results = simplejson.loads(urllib2.urlopen(url).read())
    return [ el for el in results['responseData']['results'] ]

def google_find_urls(keyword):
    """URLs for the given search term as returned by Google"""
    return [ result['url'] for result in google_search(keyword) ]
 
def find_rss_feeds(url):
    """<link> elements with type="application/rss+xml"""
    try:
        content = urllib2.urlopen(url).read()
    except urllib2.HTTPError:
        return []

    links = SoupStrainer('link', attrs={'type': 'application/rss+xml'})

    return [ dict(tag.attrs)['href']
        for tag in BeautifulSoup(content, parseOnlyThese=links) ]

def find_feeds(keyword):
    """List of RSS urls for the given keyword"""
    feeds = []

    for url in google_find_urls(keyword):
        feeds.extend(find_rss_feeds(url))

    return feeds

class TestBase(unittest.TestCase):
    
    def test_slashdot(self):
        self.failUnless('http://rss.slashdot.org/Slashdot/slashdot'
            in find_feeds('slashdot'))

if __name__ == "__main__":
    unittest.main()

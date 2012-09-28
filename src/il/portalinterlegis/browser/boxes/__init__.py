# -*- coding: utf-8 -*-
from manager import get_template
import feedparser
import urllib2, urllib
from zope.app.component.hooks import getSite

class LastNews(object):

    def __init__(self, kind):
        self.kind = kind

    def __call__(self, context):
        template = get_template("lastnews.html")
        # TODO: fazer busca no catalogo por tag
        busca = context.portal_catalog(portal_type="News Item",
                                       sort_on='Date',sort_order='reverse')[:5]
        news = [(noticia.getObject().title, noticia.getURL()) for noticia in busca]
        # TODO: traduzir kind de tag para class css
        return template.render(news=news, css_class=self.kind)

class Events(object):
    
    def kind(self, event):
        # TODO ...
        return "comunicacao"

    def __call__(self, context):
        template = get_template("icalendar.html")
        # TODO: fazer busca no catalogo por tag
        busca = context.portal_catalog(portal_type="Event",
                                       sort_on='Date',sort_order='reverse')[:2]
        events = [(event.getObject().title, event.getURL(), self.kind(event)) for event in busca]
        # TODO: traduzir kind de tag para class css
        return template.render(events=events) 

def colab(context):

    # from http://stackoverflow.com/a/34116
    proxy = getSite().getProperty('proxy')
    proxy_handler = urllib2.ProxyHandler({'http': proxy})
    auth = urllib2.HTTPBasicAuthHandler()
    opener = urllib2.build_opener(proxy_handler, auth, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

    def feed(url):
        conn = urllib2.urlopen(url)
        feed = feedparser.parse(conn.read())
        return feed['entries'][:3]
    return get_template('colab.html').render(
        colaboracoes=feed('http://colab.interlegis.leg.br/rss/colab/latest/'),
        discussoes=feed('http://colab.interlegis.leg.br/rss/threads/hottest/'))

def socialnetworks(context):
    return get_template('socialnetworks.html').render()

def video(context):
    return get_template('boxvideos.html').render()

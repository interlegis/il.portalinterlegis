# -*- coding: utf-8 -*-
import re
import urllib2

import feedparser
from DateTime import DateTime
from manager import get_template
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

meses = ['', 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
         'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez',]

class Events(object):

    def kind(self, event):
        # TODO ...
        return "comunicacao"

    def __call__(self, context):

        def event_tuple(results):
            return [(event.title,
                     event.absolute_url(),
                     event.startDate.day(),
                     meses[event.startDate.month()],
                     self.kind(event), ) for event in [brain.getObject()
                                                       for brain in results]]

        important_events = event_tuple(context.portal_catalog(
            {'start': {'query': DateTime(), 'range': 'min'}},
            portal_type="Event",
            sort_on='Date',
            Subject=('evento importante'))[:1])
        events = event_tuple(context.portal_catalog(
            {'start': {'query': DateTime(), 'range': 'min'}},
            portal_type="Event",
            sort_on='Date')[:4])

        for e in important_events:
            if e in events:
                events.remove(e)

        template = get_template("events.html")
        return template.render(important_events=important_events,
                               events=events)

colab_filter_entries_res = (
    (re.compile('changeset: \[.*\] - (.*)'), u'código'),
    (re.compile('ticket: [^-]+ - (.*)'), u'tíquete'),
    )

def colab(context):

    proxy = getSite().getProperty('proxy')
    if proxy:
        # from http://stackoverflow.com/a/34116
        proxy_handler = urllib2.ProxyHandler({'http': proxy})
        auth = urllib2.HTTPBasicAuthHandler()
        opener = urllib2.build_opener(proxy_handler, auth, urllib2.HTTPHandler)
        urllib2.install_opener(opener)

    def feed(url):
        try:
            conn = urllib2.urlopen(url)
            feed = feedparser.parse(conn.read())
            entries = filter_entries(feed)
            return entries[:3]
        except:
            # pode haver problema com proxy.
            # Não podemos quebrar tudo por conta disso.
            return []

    def filter_entries(feed):
        entries = filter(lambda e: 'Merge branch' not in e['title'],
                         feed['entries'])
        for entry in entries:
            for (pattern, prefix) in colab_filter_entries_res:
                m = pattern.match(entry['title'])
                if m:
                    entry['title'] = "%s: %s" % (prefix, m.group(1))
        return entries

    # TODO: usar: http://colab.interlegis.leg.br/rss/threads/hottest/
    # mas o RSS está com problema
    return get_template('colab.html').render(
        colaboracoes=feed('http://colab.interlegis.leg.br/rss/colab/latest/'),
        discussoes=feed('http://colab.interlegis.leg.br/rss/threads/latest/'))

def socialnetworks(context):
    return get_template('socialnetworks.html').render()

def video(context):
    return get_template('boxvideos.html').render()

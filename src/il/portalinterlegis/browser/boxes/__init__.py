# -*- coding: utf-8 -*-
import re
import urllib2

import feedparser
from DateTime import DateTime
from manager import get_template
from zope.app.component.hooks import getSite

class Events(object):

    def kind(self, event):
        # TODO ...
        return "comunicacao"

    def __call__(self, context):

        def event_tuple(results):
            return [(event.title,
                     event.absolute_url(),
                     event.startDate.day(),
                     event.startDate.month(),
                     self.kind(event),) for event in [brain.getObject()
                                                       for brain in results]]

        important_events = event_tuple(context.portal_catalog(
            {'end': {'query': DateTime(), 'range': 'min'}},
            portal_type="Event",
            sort_on='start',
            Subject=('evento importante'))[:1])
        events = event_tuple(context.portal_catalog(
            {'end': {'query': DateTime(), 'range': 'min'}},
            portal_type="Event",
            sort_on='start')[:4])

        for e in important_events:
            if e in events:
                events.remove(e)
        events = events[:3]

        template = get_template("events.html")
        return template.render(important_events=important_events,
                               events=events)

colab_filter_entries_res = (
    (re.compile('changeset: \[.*\] - (.*)'), u'código'),
    (re.compile('ticket: .+ - (.*)'), u'tíquete'),
    (re.compile('thread: .+ - (.*)'), u'mensagem')
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

def interlegis_na_midia(context):
    path = '/'.join(context['interlegisnamidia'].getPhysicalPath())
    busca = context.portal_catalog.searchResults(
        path={"query": path, "depth": 1},
        sort_on='Date',
        sort_order='reverse',
        )[:3]
    entries = [(noticia.getObject().title, noticia.getURL()) for noticia in busca]
    return get_template('interlegis_na_midia.html').render(entries=entries)

def noticias_e_artigos_interlegis(context):
    template = get_template('noticias-e-artigos-interlegis.html')
    busca = context.portal_catalog.searchResults(
        portal_type="News Item",
        sort_on='Date',
        sort_order='reverse',)[:3]
    entries = [(noticia.getObject().title, noticia.getURL()) for noticia in busca]
    # TODO: traduzir kind de tag para class css
    return template.render(entries=entries)

def consultoria_e_informacao(context):
    return get_template('consultoria-e-informacao.html').render()

def produtos_de_tecnologia(context):
    return get_template('produtos-de-tecnologia.html').render()

def capacitacao_ilb(context):
    return get_template('capacitacao-ilb.html').render()

def relacionamento(context):
    return get_template('relacionamento.html').render()

def video(context):
    return get_template('boxvideos.html').render()


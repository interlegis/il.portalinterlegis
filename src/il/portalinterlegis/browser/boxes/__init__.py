# -*- coding: utf-8 -*-
from manager import get_template
import feedparser

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

def colab(context):
    def feed(url):
        feed = feedparser.parse(url)
        return feed['entries'][:3]
    return get_template('colab.html').render(
        colaboracoes=feed('http://colab.interlegis.leg.br/rss/colab/latest/'),
        discussoes=feed('http://colab.interlegis.leg.br/rss/threads/hottest/'))

def socialnetworks(context):
    return get_template('socialnetworks.html').render()

def video(context):
    return get_template('boxvideos.html').render()

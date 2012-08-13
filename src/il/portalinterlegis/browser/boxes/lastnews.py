# -*- coding: utf-8 -*-
from manager import get_template


class LastNews(object):

    def __init__(self, kind):
        self.kind = kind

    def __call__(self, context):
        template = get_template("lastnews.html")
        # TODO: fazer busca no catalogo por tag
        news = [
            (u"UVESC reafirma interesse em ampliar parceria com Interlegis", "news/TODO"),
            (u"Parlamento do Timor Leste quer apoio do Interlegis para se organizar", "news/TODO"),
            (u"Itaperuna deve sediar oficina de Portal Modelo para 15 cidades", "news/TODO"),
            (u"UVESC reafirma interesse em ampliar parceria com Interlegis", "news/TODO"),
            (u"Parlamento do Timor Leste quer apoio do Interlegis para se organizar", "news/TODO"),
            ]
        # TODO: traduzir kind de tag para class css
        return template.render(news=news, css_class=self.kind)

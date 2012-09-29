news = context.portal_catalog(portal_type='News Item')
pilares = {
    u'INFORMAÇÃO' : [u'INFORMAÇÃO'],
    u'CAPACITAÇÃO': [u'CAPACITAÇÃO', u'CAPACITAÇÂO'],
    u'TECNOLOGIA': [u'TECNOLOGIA'],
    }
separador = ' - '
agrupados = {cat: [] for cat in pilares}
for brain in news:
    obj = brain.getObject()
    title = obj.title
    if separador in title:
        cat, title = title.split(separador, 1)
        if cat in pilares:
            obj.setTitle(title)
            obj.setSubject(set(obj.Subject() + (cat, )))
            agrupados[cat].append(obj)

for cat in pilares:
    print '### %s ###' % cat
    for o in agrupados[cat]:
        print o.title, o.Subject()


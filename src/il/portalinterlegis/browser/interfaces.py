# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import Interface

# TODO: tive de mover isso pra ca (veio de boxes) por causa de um import circular
template_dict = {}
def template(t):
    def f(cls):
        template_dict[cls] = t
        return cls
    return f

class IThemeSpecific(Interface):
    """Marker interface that defines a Zope 3 browser layer.
       If you need to register a viewlet only for the
       "il.portalinterlegis" theme,
       this interface must be its layer.
    """

# HOMES

class IComunidadeLegislativa(Interface):
    "Marker interface para home"

class IInformacao(Interface):
    "Marker interface para home"

class ICapacitacao(Interface):
    "Marker interface para home"

class ITecnologia(Interface):
    "Marker interface para home"

class IComunicacao(Interface):
    "Marker interface para home"

# BOX INTERFACES

@template('''
      <div class="simple-box">
        <h2>%(title)s</h2>
        <h3 class="icon-news"><a href="">%(subtitle)s</a></h3>
        <p>
          %(text)s
        </p>
      </div>''')
class ISimpleBox(Interface):
    title = schema.TextLine(title=u"Título", required=True)
    subtitle = schema.TextLine(title=u"Subtítulo", required=True)
    text = schema.TextLine(title=u"Texto", required=True)

@template('''
      <div id= "container">

		<div class="carousel example-5">
		  <ul>
			<li>
              <a href="">
                <img src="/portal/++theme++il.portalinterlegis/temp/images/1.jpg" alt="ex1" width="340" height="215" />
                <div class="carousel-text">
                  <h3><b>Envie</b> Notícias</h3>
                  <p>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean sed est eu mauris lacinia molestie. Integer eu ultricies nisl.
                  </p>
                </div>
              </a>
            </li>
			<li>
              <a href="">
                <img src="/portal/++theme++il.portalinterlegis/temp/images/caneca.jpg" alt="ex2" width="340" height="215" />
                <div class="carousel-text">
                  <h3><b>Mais</b> Novidades</h3>
                  <p>
                    Maecenas vehicula magna eget eros dictum fringilla. In hac habitasse platea dictumst. Aenean vestibulum ligula neque. Ut id varius ante.
                  </p>
                </div>
              </a>
            </li>
			<li>
              <a href="">
                <img src="/portal/++theme++il.portalinterlegis/temp/images/interlegis.jpg" alt="ex3" width="340" height="215" />
                <div class="carousel-text">
                  <h3><b>Ainda</b> muito <b>mais...</b></h3>
                  <p>
                    Aenean pellentesque consectetur neque. Integer ultrices tincidunt odio ut adipiscing. Aliquam erat volutpat. Morbi auctor faucibus odio id cursus.
                  </p>
                </div>
              </a>
            </li>
		  </ul>
		</div>

	  </div>
''')
class ICarousel(Interface):
    pass

@template('''
      <h2 class="box-header">Andamento do Interlegis</h2>
      TODO: AGENDA... <br/><br/><br/>
''')
class ICalendar(Interface):
    pass

@template('''
      <h2 class="box-header">Acompanhe o Interlegis</h2>
      TODO: Acompanhe o Interlegis... <br/><br/><br/>
''')
class IAcompanheOInterlegis(Interface):
    pass

@template('''
      TODO: tabs dos pilares <br/><br/><br/>
''')
class ITabsPilares(Interface):
    pass

@template('''
      <h2 class="box-header">Destaque</h2>
      TODO: <br/><br/><br/>
''')
class IHighlight(Interface):
    pass

def box_schemas():
    return template_dict.keys()

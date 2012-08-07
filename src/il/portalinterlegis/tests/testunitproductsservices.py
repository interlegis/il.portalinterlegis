# -*- coding: utf-8 -*-
from mock import patch

from il.portalinterlegis.browser.boxes.manager import Box, DtRow, BoxAware
from il.portalinterlegis.browser.boxes.carousel import Carousel
from il.portalinterlegis.browser.boxes.interfaces import ICarouselItem

from itertools import count
from mock import MagicMock as Mock

from differenttestcase import DifferentTestCase

KIND = 'products-and-services'

class TestProductsServices(DifferentTestCase):

    def test_render_basic(self):
        """Given a certain IAnnotations state (our DB) assert a redered output.
        """
        context = object()
        with patch('il.portalinterlegis.browser.boxes.manager.IAnnotations') as IAnnotations:
            IAnnotations.return_value = {BoxAware.ALL_BOXES_KEY: {
                Carousel(KIND, 0, context)._panels_key(): [1, 2],
                Box(ICarouselItem, 1).id: dict(
                    target = "TARGET_1",
                    image = "IMG_1", # ignoring for now
                    title = "TITLE_1",
                    text = "TEXT_1",
                ),
                Box(ICarouselItem, 2).id: dict(
                    target = "TARGET_2",
                    image = "IMG_2", # ignoring for now
                    title = "TITLE_2",
                    text = "TEXT_2",
                ),
            }}
            self.assertMultiLineEqual(u'''
<div class="products-services-container">
  <h2>Produtos e Serviços</h2>
  <div class="next-previous-buttons">
    <input type="button" value="Previous" />
    <input type="button" value="Next" />
  </div>
  <div class="products-services">
    <ul>
      <li>
        <a class="products-services-item" title="Saiba mais sobre TITLE_1" href="TARGET_1">
          <h3 class="icon-home">TITLE_1</h3>
        </a>
        TEXT_1
      </li>
      <li>
        <a class="products-services-item" title="Saiba mais sobre TITLE_2" href="TARGET_2">
          <h3 class="icon-home">TITLE_2</h3>
        </a>
        TEXT_2
      </li>
    </ul>
  </div>
</div>
'''.strip('\n'), Carousel(KIND, 0, context).render())
            IAnnotations.assert_called_with(context)

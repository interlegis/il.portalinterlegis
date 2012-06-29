# -*- coding: utf-8 -*-
from mock import patch

from il.portalinterlegis.browser.boxes.manager import Box, DtRow, BoxAware
from il.portalinterlegis.browser.boxes.carousel import Carousel
from il.portalinterlegis.browser.boxes.interfaces import ICarouselItem

from itertools import count
from mock import MagicMock as Mock

from differenttestcase import DifferentTestCase

class TestCarousel(DifferentTestCase):

    def test_render_basic(self):
        """This is a semi-integration test: given a certain IAnnotations state (our DB)
        assert a redered output
        """
        context = object()
        with patch('il.portalinterlegis.browser.boxes.manager.IAnnotations') as IAnnotations:
            IAnnotations.return_value = {BoxAware.ALL_BOXES_KEY: {
                Carousel(0, context)._panels_key(): [1, 2],
                Box(ICarouselItem, 1).id: dict(
                    target = "TARGET_1",
                    image = "IMG_1",
                    title = "TITLE_1",
                    text = "TEXT_1",
                ),
                Box(ICarouselItem, 2).id: dict(
                    target = "TARGET_2",
                    image = "IMG_2",
                    title = "TITLE_2",
                    text = "TEXT_2",
                ),
            }}
            self.assertMultiLineEqual('''
<div class="carousel-container">
  <div class="carousel">
    <ul>
      <li>
        <a href="TARGET_1">
          <img src="IMG_1" width="340" height="215" />
          <div class="carousel-text">
            <h3>TITLE_1</h3>
            <p>
              TEXT_1
            </p>
          </div>
        </a>
      </li>
      <li>
        <a href="TARGET_2">
          <img src="IMG_2" width="340" height="215" />
          <div class="carousel-text">
            <h3>TITLE_2</h3>
            <p>
              TEXT_2
            </p>
          </div>
        </a>
      </li>
    </ul>
  </div>
</div>
'''.strip('\n'), Carousel(0, context).render())
            IAnnotations.assert_called_with(context)

    def test_multiple_carousel_panels_are_independant(self):
        """Make sure the panels of different carousels do not mix
        with one another after edit operations.
        """
        annotations = {}
        context = object()
        with patch('il.portalinterlegis.browser.boxes.manager.IAnnotations') as IAnnotations:
            IAnnotations.return_value = annotations
            carousel_0 = Carousel(0, context)
            carousel_1 = Carousel(1, context)

            carousel_0.add_item()
            carousel_0.add_item()
            carousel_0.add_item()
            self.assertEqual(carousel_0.panels, [2, 1, 0])
            self.assertEqual(carousel_1.panels, [])
            carousel_0.remove_item('zzzzz_1')
            self.assertEqual(carousel_0.panels, [2, 0])
            self.assertEqual(carousel_1.panels, [])
            carousel_1.add_item()
            carousel_1.add_item()
            self.assertEqual(carousel_0.panels, [2, 0])
            self.assertEqual(carousel_1.panels, [3, 1])
            carousel_1.remove_item('zzzzz_3')
            self.assertEqual(carousel_0.panels, [2, 0])
            self.assertEqual(carousel_1.panels, [1])
            carousel_0.add_item()
            carousel_0.add_item()
            carousel_1.add_item()
            self.assertEqual(carousel_0.panels, [4, 3, 2, 0])
            self.assertEqual(carousel_1.panels, [5, 1])

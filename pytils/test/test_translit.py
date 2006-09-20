# -*- coding: utf-8 -*-
# License: GNU GPL2
# Author: Pythy <the.pythy@gmail.com>
"""
Unit-tests for pytils.translit
"""


__id__ = __revision__ = "$Id$"
__url__ = "$URL$"

import unittest

import pytils

class TranslitTestCase(unittest.TestCase):
    """
    Test case for pytils.translit
    """

    def ckTransl(self, in_, out_):
        """
        Checks translify
        """
        self.assertEquals(pytils.translit.translify(in_), out_)

    def ckDetransl(self, in_, out_):
        """
        Checks detranslify
        """
        self.assertEquals(pytils.translit.detranslify(in_), out_)

    def ckSlug(self, in_, out_):
        """
        Checks slugify
        """
        self.assertEquals(pytils.translit.slugify(in_), out_)

    def testTransliteration(self):
        """
        Unit-test for transliterations
        """
        self.ckTransl(u"тест", 'test')
        self.ckTransl(u"проверка", 'proverka')
        self.ckTransl(u"транслит", 'translit')
        self.ckTransl(u"правда ли это", 'pravda li eto')

    def testDetransliteration(self):
        """
        Unit-test for detransliterations
        """
        self.ckDetransl('test', u"тест")
        self.ckDetransl('proverka', u"проверка")
        self.ckDetransl('translit', u"транслит")

    def testSlug(self):
        """
        Unit-test for slugs
        """
        self.ckSlug(u"ТеСт", 'test')
        self.ckSlug(u"Проверка связи", 'proverka-svyazi')
        self.ckSlug(u"me&you", 'me-and-you')
        self.ckSlug(u"и еще один тест", 'i-esche-odin-test')

if __name__ == '__main__':
    unittest.main()

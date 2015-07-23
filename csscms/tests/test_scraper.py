import unittest
from csscms import properties_scraper as scraper


class PropertyScraperTestCase(unittest.TestCase):

    def test_normalize_w3c_link(self):
        res = scraper.normalize_w3c_link('pr_text_color.asp')
        res2 = scraper.normalize_w3c_link('css3_pr_text_color.asp')
        self.assertEqual(res, 'text-color')
        self.assertEqual(res2, 'text-color')

    def test_strip_all_prefixes(self):
        res = scraper.strip_all_prefixes('font-font-gen-tab-')
        res2 = scraper.strip_all_prefixes('class-')
        self.assertEqual(res, '')
        self.assertEqual(res2, '')

import unittest
from csscms import validations
from csscms.css_options import css_opts


class ValidationsTestCase(unittest.TestCase):

    def setUp(self):
        self.helper = validations.ValidationHelpersMixin()

    def test_is_valid_badprops(self):
        for opt in css_opts['bad_properties']:
            self.assertFalse(
                self.helper._is_valid_css_declaration(opt))

    def test_is_valid_badvalues(self):
        for opt in css_opts['bad_values']:
            self.assertFalse(
                self.helper._is_valid_css_declaration(opt))

    def test_is_valid_hyphen(self):
        self.assertFalse(self.helper._is_valid_css_declaration('-foobar'))

    def test_is_hex_true(self):
        res = self.helper._is_hex('#fff')
        res2 = self.helper._is_hex('#ffffff')
        self.assertTrue(res)
        self.assertTrue(res2)

    def test_is_hex_false(self):
        res = self.helper._is_hex('fff')
        res2 = self.helper._is_hex('ffffff')
        res3 = self.helper._is_hex('ff03')
        self.assertFalse(res)
        self.assertFalse(res2)
        self.assertFalse(res3)

    def test_is_percentage(self):
        res = self.helper._is_percentage('10%')
        res2 = self.helper._is_percentage('10')
        self.assertTrue(res)
        self.assertFalse(res2)

    def test_is_int(self):
        res = self.helper._is_int(3)
        res2 = self.helper._is_int(0)
        res3 = self.helper._is_int(9999)
        self.assertTrue(res)
        self.assertTrue(res2)
        self.assertTrue(res3)
        self.assertFalse(self.helper._is_int(float(3)))
        self.assertFalse(self.helper._is_int(float(0)))
        self.assertFalse(self.helper._is_int(float(9999)))

    def test_is_float(self):
        res = self.helper._is_float(3.0)
        res2 = self.helper._is_float(0.0)
        res3 = self.helper._is_float(9999.0)
        self.assertTrue(res)
        self.assertTrue(res2)
        self.assertTrue(res3)

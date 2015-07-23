import unittest
from csscms import parser
from os import getcwd


class ParserTestCase(unittest.TestCase):

    def setUp(self):
        self.helper = parser.InputBuilder(
            '{}/csscms/tests/css_test.css'.format(getcwd()))

    def test_parse_media(self):
        # TODO
        pass

    def test_parse_atrule(self):
        # TODO
        pass

    def test_strip_quotes(self):
        # TODO
        pass

    def test_convert_odd_types(self):
        # TODO
        pass

    def test_get_dropdown_html(self):
        # TODO
        pass

    def test_is_cruft(self):
        res = self.helper._is_cruft('S')
        res2 = self.helper._is_cruft('DELIM')
        self.assertTrue(res)
        self.assertTrue(res2)

    def test_wrap_input_html(self):
        # TODO
        pass

    def test_get_new_type(self):
        token_types = {
            '#fff': 'HASH',
            '#ff0000': 'HASH',
            '10%': 'PERCENTAGE',
            '3.0': 'FLOAT',
            '.': 'IDENT',
        }
        for token_type, expected in token_types.iteritems():
            res = self.helper._get_new_type(token_type)
            self.assertEqual(res, expected)

    def test_get_token_value(self):
        # TODO
        pass

    def test_get_form_html_data(self):
        # TODO
        pass

    def test_get_at_keyword_type(self):
        at_types = [
            ('import', {'uri': '@foo'}),
            ('import', {'media': '@foo'}),
            ('keyframes', {'keyframes': []}),
            ('media', {'rules': []}),
            ('foo', {'at_keyword': '@foo'})
        ]
        for at_type in at_types:
            expected, obj = at_type
            res = self.helper._get_at_keyword_type(obj)
            self.assertEqual(res, expected)

    def test_group_keyframe_tokens(self):
        # TODO
        pass

    def test_generate_keyframes_declarations(self):
        # TODO
        pass

    def test_generate_mediaquery_declarations(self):
        # TODO
        pass

    def test_generate_import_declarations(self):
        # TODO
        pass

    def test_generate_regular_declarations(self):
        # TODO
        pass

    def test_get_generator(self):
        # TODO
        pass

    def test_generate(self):
        # TODO
        pass

    def test_save(self):
        # TODO
        pass

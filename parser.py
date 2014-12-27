import tinycss
import css_properties
from pprint import pprint


DEBUG = True
css_opts = {
    'bad_properties': [
        'filter',
        'ms-filter',
    ],
    'bad_values': [
        'progid',
        'Microsoft',
    ],
    'xforms': [
        'matrix', 'matrix3d', 'skewX', 'skewY', 'perspective',
        'translate', 'translateX', 'translateY', 'translateZ', 'translate3d',
        'scale', 'scaleX', 'scaleY', 'scaleZ', 'scale3d',
        'rotate', 'rotateX', 'rotateY', 'rotateZ', 'rotate3d'
    ],
    'odd_props': {
        '%': 'PERCENTAGE',
        'number': 'INTEGER',
        'length-v': 'INTEGER',
        'length-h': 'INTEGER',
        'length': 'INTEGER',
        'color': 'HASH',
        'background-color': 'HASH',
        'x%': 'PERCENTAGE',
        'y%': 'PERCENTAGE',
        'xpos': 'INTEGER',
        'ypos': 'INTEGER',
        'time': 'FLOAT',
        'url': 'URI',
        'h-shadow': 'INTEGER',
        'v-shadow': 'INTEGER',
        'blur': 'INTEGER',
        'x-axis': 'INTEGER',
        'y-axis': 'INTEGER',
        'z-axis': 'INTEGER',
        'keyframename': 'STRING',
    },
    'composites': [
        'font', 'background'
    ],
    # @import types
    'media_types': [
        'print', 'tv', 'all', 'screen', 'projection',
    ],
    # @keyword types.
    'at_types': [
        'import', 'media', 'keyframes'
    ],
    # Properties assigned to each Token; taken from:
    # pythonhosted.org/tinycss/parsing.html#tinycss.token_data.Token.type
    # Maps a Token class "type" to an actual relevant input field.

    # Also see http://dev.w3.org/csswg/css-syntax/#typedef-ident-token
    # for CSS specs on token types.
    'types': {
        ':': '',
        'S': '',
        'IDENT': '',
        'RGBHSV': '<input type="number" min="0" max="255" name="{name}" placeholder="{placeholder}">',
        'DEG': '<input type="number" min="0" max="360" name="{name}" placeholder="{placeholder}">',
        'FLOAT': '<input type="number" min="0" max="1" name="{name}" placeholder="{placeholder}">',
        'INTEGER': '<input type="number" name="{name}" placeholder="{placeholder}">',
        'NUMBER': '<input type="number" name="{name}" placeholder="{placeholder}">',
        'PERCENTAGE': '<input type="number" min="0" max="100" name="{name}" value="{placeholder}">',
        'HASH': '<input type="color" value="{placeholder}" name="{name}">',
        'ATKEYWORD': '',
        'URL': '<input type="file" name="{name}">',
        'URI': '<input type="file" name="{name}">',
        'UNICODE-RANGE': '',
        'FUNCTION': '',
        'OPTION': '<option value="{value}" {selected}>{placeholder}</option>',
        'BOOLEAN': '<input type="checkbox" checked={is_checked}>',
        'DIMENSION': '<input type="number" name="{name}"  placeholder="{placeholder}">',
        'STRING': '<input type="text" name="{name}" placeholder="{placeholder}">',
        'DELIM': '',
        'VISIBLE': '',
    },
}


class MissingTokenType(Exception):
    def __init__(self):
        print ('Invalid token type: please add a '
               'new one to the token types config.')


class MissingAtKeywordType(Exception):
    def __init__(self):
        print ('Invalid @ keyword type. Options are: {}'.format(
            ' ').join(css_opts['at_types']))


class CSSParserMixin():

    """Custom parsing beyond that of tinycss"""

    def _parse_gradient(self, function, grad_type):
        _inputs = []
        function = function.replace(
            grad_type + '(', '').replace(')', '').split(' ')
        for token in function:
            token = token.replace(' ', '').split(',')
            for k, sub_token in enumerate(token):
                if self._is_percentage(sub_token):
                    label = '{}-percent-{}'.format(grad_type, k)
                    _inputs.append(
                        [label, css_opts['types']['PERCENTAGE'].format(
                            name=label,
                            placeholder=sub_token[:-1])])
                elif self._is_hex(sub_token):
                    label = '{}-hex-{}'.format(grad_type, k)
                    _inputs.append(
                        [label, css_opts['types']['HASH'].format(
                            name=label,
                            placeholder=sub_token)])
        return _inputs

    def _parse_rgb(self, function):
        _inputs = []
        function = function.replace('rgba(', '').replace(')', '').split(',')
        _inputs.append(['red', css_opts['types']['RGBHSV'].format(
            name='red', placeholder=function[0])])
        _inputs.append(['green', css_opts['types']['RGBHSV'].format(
            name='green', placeholder=function[1])])
        _inputs.append(['blue', css_opts['types']['RGBHSV'].format(
            name='blue', placeholder=function[2])])
        return _inputs

    def _parse_rgba(self, function):
        _inputs = []
        function = function.replace('rgba(', '').replace(')', '').split(',')
        _inputs.append(['red', css_opts['types']['RGBHSV'].format(
            name='red', placeholder=function[0])])
        _inputs.append(['green', css_opts['types']['RGBHSV'].format(
            name='green', placeholder=function[1])])
        _inputs.append(['blue', css_opts['types']['RGBHSV'].format(
            name='blue', placeholder=function[2])])
        _inputs.append(['alpha', css_opts['types']['INTEGER'].format(
            name='alpha', placeholder=function[3])])
        return _inputs

    def _parse_media_query(self, function):
        # TODO
        return ''
        pass

    def _parse_transform(self, function):
        _inputs = []
        function = function.replace('(', ' ').replace(')', ' ').split(' ')
        for k, token in enumerate(function):
            # Filter out transforms, until we can do selects/options TODO
            input_html = ''
            if token and token not in css_opts['xforms']:
                token = token.replace(',', '')
                kwargs = {'name': token, 'placeholder': token}
                if self._is_float(token):
                    input_html = css_opts['types']['FLOAT'].format(**kwargs)
                elif token.endswith('px'):
                    input_html = css_opts['types']['NUMBER'].format(**kwargs)
                elif token.endswith('deg'):
                    input_html = css_opts['types']['DEG'].format(**kwargs)
                elif self._is_int(token):
                    input_html = css_opts['types']['INTEGER'].format(**kwargs)
                else:
                    continue
                # Add after to keep DRY
                _inputs.append(['{}: #{}'.format(function[0], k), input_html])
        return _inputs

    def _parse_css_function_inputs(self, function):
        """Parses arguments of a CSS function into their respective
        matching inputs. Deviates from tinycss style because of necessary
        substring parsing / matching.

        e.g. rgba(255, 0, 0, 0.4) becomes:

        <input type="number" min="0" max="255">
        <input type="number" min="0" max="255">
        <input type="number" min="0" max="1">
        <input type="number" min="0" max="0.4">

        or linear-gradient(top, #444 0%, #444 100%), becomes:

        <select name="" id=""><option value="">...</option></select>
        <input type="color">
        <input type="number" min="0" max="100">
        <input type="color">
        <input type="number" min="0" max="100">

        """
        inputs, html = [], ''

        if function.startswith('rgba'):
            inputs += self._parse_rgba(function)
        elif function.startswith('rgb'):
            inputs += self._parse_rgb(function)
        elif function.startswith('linear-gradient'):
            inputs += self._parse_gradient(function, 'linear-gradient')
        elif function.startswith('radial-gradient'):
            inputs += self._parse_gradient(function, 'radial-gradient')
        elif filter(lambda prop: function.startswith(prop), css_opts['xforms']):
            inputs += self._parse_transform(function)

        # Finally, build up individual surrounding labels + input
        # for each input "argument"
        for name, _input in inputs:
            html += self.default_input_html.format(
                name=name, input_html=_input)
        return html


class ValidationHelpersMixin():

    """Just some predicate filters..."""

    def _is_valid_css_property(self, prop_name):
        """Allows for arbitrary validation, with some sane defaults"""
        return (prop_name not in css_opts['bad_properties']
                # No vendor prefixed props.
                and not prop_name.startswith('-')
                and prop_name not in self.unwanted_props
                and prop_name not in css_opts['bad_values'])

    def _is_hex(self, val):
        """Checks for a valid hex string, e.g. `#fff` or `#ff0000`"""
        if val.startswith('#') and (len(val) == 4 or len(val) == 7):
            return True
        return False

    def _is_percentage(self, val):
        """Checks if val is a percentage number (e.g. 10%, 10.0%)."""
        return val.endswith('%')

    def _is_int(self, val):
        """Checks if val is an integer."""
        try:
            self._is_float(val)
            if '.' in str(val):
                return False
            return True
        except ValueError:
            return False

    def _is_float(self, val):
        """Checks if val is a float."""
        try:
            float(val)
            return True
        except ValueError:
            return False


class InputBuilder(CSSParserMixin, ValidationHelpersMixin):

    """
    Convention: all public methods return `self` to allow for chaining.

    TODO: tests!

    TODO: implement boolean field for !important,
    important via `priority` property.

    TODO: better way to handle combos of select dropdowns AND input fields
    (e.g. image css props, that require url() or default options...)

    TODO: handle @media (queries)

    TODO: handle `inset` option

    TODO: docs, docstrings

    TODO: handle @keyframes

    TODO: accurately handle multiple transform declarations

    TODO: handle composite properties (e.g. font: '', or background: '')

    """

    def __init__(self, filename, custom_input_html=None, show_empty=False):
        self.use_value = True
        self._generated_data = None
        self.css_input_wrapper_class = 'css-func'
        self.unwanted_props = []
        self.show_empty_declarations = show_empty
        self.custom_input_html = custom_input_html
        self.parser = tinycss.make_parser('page3')
        self.stylesheet = self.parser.parse_stylesheet_file(filename)
        self.surrounding_html = '<div class="{}">{}</div>'
        self.input_container_html = ('<div class="selector-group">\n'
                                     '<span class="selector-label">'
                                     '{} {}</span>\n{code}</div>\n')
        self.default_input_html = ('<label>\n<em>{name}</em>'
                                   '\n{input_html}\n</label>\n')

    def _strip_quotes(self, val):
        """Normalize properties with beginning or
        trailing quotations, like `content: ""`
        """
        if type(val) != 'str':
            return val
        if val.startswith('"'):
            val = val[1:]
        if val.endswith('"'):
            val = val[:-1]
        return val

    def _convert_odd_types(self, value):
        try:
            return css_opts['odd_props'][value]
        except KeyError:
            return None

    def _get_dropdown_html(self, props, name='', token=None):
        """Takes name and value, then builds
        matching select > option html"""
        # Accompanying input html required for some
        # non-dropdown complementary fields
        non_dropdown_html = ''
        dropdown_html = '<select name="{}">'.format(name)
        for prop in props:
            # One off cases where some value should be represented
            # by a different field type
            if prop in css_opts['odd_props']:
                new_token_type = self._convert_odd_types(prop)
                if new_token_type is not None:
                    non_dropdown_html += self._get_input_html(
                        new_token_type, prop, prop)
            else:
                # Build the /actual/ option html.
                dropdown_html += self._get_input_html(
                    'OPTION', prop, prop, selected='')
        dropdown_html += '</select>'
        return (non_dropdown_html + (
            '<em class="or-divider">or</em>'
            if non_dropdown_html else '') + dropdown_html)

    def _get_input_html(self, token_type, prop, value, **kwargs):
        value = self._strip_quotes(value)
        # Functions need to be parsed a second time, separately.
        try:
            if token_type == 'FUNCTION':
                input_html = self._parse_css_function_inputs(value)
            else:
                input_html = css_opts['types'][token_type].format(
                    name=prop, placeholder=value,
                    value=value if self.use_value else '', **kwargs)
            return input_html
        except KeyError:
            raise MissingTokenType

    def _wrap_input_html(self, **kwargs):
        """Wraps form field grouping with surrounding html"""
        if self.custom_input_html:
            # Allow arbitrary custom html, so long as the kwargs
            # match up the format kwargs -- otherwise error will be thrown.
            html = self.custom_input_html.format(**kwargs)
        else:
            html = self.default_input_html.format(**kwargs)
        return self.surrounding_html.format(self.css_input_wrapper_class, html)

    def _get_form_html_data(self, token, prop_name):
        """Generates kwargs data to be used by html builder"""
        # Normalize single vs multiple valued declarations
        try:
            # Token props:
            # 'as_css', 'column', 'is_container', 'line', 'type', 'unit', 'value'
            prop_key = css_properties.rules[prop_name]
            # Only overwrite string if it's not container type
            if prop_key['dropdown']:
                html = self._get_dropdown_html(
                    prop_key['values'], name=prop_name, token=token.type)
            else:
                html = self._get_input_html(token.type, prop_name, token.value)
        except KeyError:
            if DEBUG:
                print '[ERROR] Property: "{}"'.format(prop_name)
            return ''
        return html

    def _get_at_keyword_type(self, ruleset):
        try:
            if ruleset.media:
                return 'import'
            elif ruleset.media_query:
                return 'media'
            elif ruleset.keyframes:
                return 'keyframes'
        except AttributeError:
            return ''

    def _generate_keyframes_declarations(self, ruleset, selector):
        # TODO
        group = {
            'selector': selector,
            'inputs': []
        }
        return group

    def _generate_mediaquery_declarations(self, ruleset, selector):
        # TODO
        group = {
            'selector': selector,
            'inputs': []
        }
        return group

    def _generate_import_declarations(self, ruleset, selector):
        group = {
            'selector': selector,
            'inputs': []
        }
        for media_type in ruleset.media:
            # All media types are basic strings except for url() declarations
            if media_type in css_opts['media_types']:
                kwargs = {
                    'name': media_type,
                    'input_html': self._get_input_html(
                        'URL', media_type, ruleset.uri)
                }
                group['inputs'].append(self._wrap_input_html(**kwargs))
        return group

    def _generate_regular_declarations(self, ruleset, selector):
        group = {
            'selector': selector,
            'inputs': []
        }
        # All declarations in the selector
        for declaration in ruleset.declarations:
            # Property, e.g. background-color
            prop_name = declaration.name
            if self._is_valid_css_property(prop_name):
                # Tokens, e.g. "[2px, solid, #4444]"
                for token in declaration.value:
                    try:
                        html = ''
                        for sub_token in token.content:
                            html += self._get_form_html_data(sub_token, prop_name)
                        # Update prop_name to add function name for more context
                        if token.function_name:
                            prop_name = '{} ({})'.format(
                                prop_name, token.function_name)
                    except AttributeError:
                        html = self._get_form_html_data(token, prop_name)
                # Add the final rendered html + labels, etc
                # Only append properties that could be
                # rendered as form fields
                if html or self.show_empty_declarations:
                    group['inputs'].append(
                        self._wrap_input_html(
                            **{'name': prop_name, 'input_html': html}))
        return group

    def generate(self):
        """Generates all html from the available stylesheet
        reference exposed by init function."""
        html_inputs = []
        for ruleset in self.stylesheet.rules:
            group_label = None
            is_at_keyword = ruleset.at_keyword is not None
            if is_at_keyword:
                # e.g. @import url('foo.css') projection, tv;
                group_label = '@' + self._get_at_keyword_type(ruleset)
                # Drill down further to determine the @ keyword type
                try:
                    label_map = {
                        '@import': self._generate_import_declarations,
                        '@media': self._generate_mediaquery_declarations,
                        '@keyframes': self._generate_keyframes_declarations
                    }
                    group = label_map[group_label](ruleset, group_label)
                except KeyError:
                    raise MissingAtKeywordType
            else:
                # The group or single selector:
                # .foo, .bar, .foo.bar {}
                group_label = ruleset.selector.as_css()
                group = self._generate_regular_declarations(ruleset, group_label)
            # Convert lists to actual html
            sel_name = ', <br>'.join(group['selector'].split(','))
            code = ' '.join(group['inputs'])
            html_inputs.append(self.input_container_html.format(sel_name, '{...}', code=code))
        # Join all data and populate global property
        self._generated_data = ''.join(html_inputs)
        return self

    def save(self, filename):
        if self._generated_data is None:
            print 'No data has been generated yet!'
            return
        with open(filename, 'w') as newfile:
            newfile.write(self._generated_data)
            newfile.write('\n')
            newfile.close()


if DEBUG:
    print '[DEBUG] Running demo'
    try:
        InputBuilder('demo/simple.css').generate().save('demo/inputs.html')
    except IOError:
        print '[ERROR] Could not load file or generate inputs'

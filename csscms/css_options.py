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
    # https://developer.mozilla.org/en-US/docs/Web/CSS/Shorthand_properties
    'shorthand': ['background', 'font', 'margin', 'border', 'border-top',
                  'border-right', 'border-bottom', 'border-left', 'box-shadow',
                  'border-width', 'border-color', 'border-style',
                  'transition', 'transform', 'padding',
                  'list-style', 'border-radius'],
    # In some edge cases, even single declarations allow
    # for css functions, which should be treated as
    # shorthand declarations instead.
    'pseudo_shorthand': ['linear-gradient', 'radial-gradient'],
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
        'IDENT': '<input type="text" value="{value}">',
        'RGBHSV': '<input type="number" min="0" max="255" name="{name}" placeholder="{placeholder}">',
        'DEG': '<input type="number" min="0" name="{name}" placeholder="{placeholder}">',
        'FLOAT': '<input type="number" min="0" max="1" name="{name}" placeholder="{placeholder}">',
        'INTEGER': '<input type="number" name="{name}" placeholder="{placeholder}">',
        'NUMBER': '<input type="number" name="{name}" placeholder="{placeholder}">',
        'PERCENTAGE': '<input type="number" min="0" name="{name}" value="{placeholder}">',
        'HASH': '<input type="color" value="{placeholder}" name="{name}">',
        'ATKEYWORD': '',
        'URL': '<input type="file" name="{name}">',
        'URI': '<input type="file" name="{name}">',
        'UNICODE-RANGE': '',
        'FUNCTION': '',
        'OPTION': '<option value="{value}" {selected}>{placeholder}</option>',
        'BOOLEAN': '<input type="checkbox" checked={checked}>',
        'DIMENSION': '<input type="number" name="{name}"  placeholder="{placeholder}">',
        'STRING': '<input type="text" name="{name}" placeholder="{placeholder}">',
        'DELIM': '',
        'VISIBLE': '',
    },
}

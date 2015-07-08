from css_options import css_opts


class ValidationHelpersMixin:

    """Just some predicate filters..."""

    def _is_valid_css_declaration(self, prop_name):
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

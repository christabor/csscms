[![Coverage Status](https://coveralls.io/repos/christabor/csscms/badge.svg?branch=master&service=github)](https://coveralls.io/github/christabor/csscms?branch=master)
[![Build Status](https://travis-ci.org/christabor/csscms.svg?branch=master)](https://travis-ci.org/christabor/csscms)
[![MIT Badge](http://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/christabor/csscms/master/LICENSE)
![Donation badge](https://img.shields.io/gratipay/christabor.svg)

CSSCMS - CSS `Content Management System`

A declarative approach to generating HTML GUIs for editing CSS properties.

All major css types have been tested with parsing (see the demo css for examples of test inputs). There are a few edge cases that might require manual updating, but the parser does quite well with very large css declarations, across most all types (media queries, keyframes, imports, etc...)

### Installation

It's not currently added to PyPi, but you can install it easily:
```python
python setup.py install
```
You may need to install using ```sudo```, depending on how your user is setup.

### Usage

Usage is quite easy. All methods return ```self```, making the interface chainable.

```python
from csscms.parser import InputBuilder
InputBuilder('mycssfile.css').generate().save('mycss-output.html')
```

### Optional customization options

Options are specified when creating a new ```InputBuilder``` object.

* **css_input_wrapper_class** (string) - input class to apply
* **unwanted_props** (list) - a list of css-properties to filter out (e.g. 'color', 'font-size')
* **custom_input_html** (string) - optional input wrapper html
* **show_empty** (bool) - override and show empty declarations (False by default.)

### Tests

Test coverage provided by [nose](https://nose.readthedocs.org/en/latest/). Run tests via ```nosetests```

import os
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()


PACKAGE = 'csscms'
VERSION = '0.2.1'


def _get_requires(filepath):
    path = '{}/{}'.format(os.path.abspath(os.path.dirname(__file__)), filepath)
    with open(path) as reqs:
        return [req for req in reqs.read().split('\n') if req]

keywords = ['csscms', 'css content management system', 'cms', 'stylesheet']
description = ('A Python tool to generate dynamic html forms for editing '
               'css files (e.g. tools), from any arbitrary css file.')
setup(
    name='csscms',
    version=VERSION,
    description=description,
    author='Chris Tabor',
    author_email='dxdstudio@gmail.com',
    maintainer='Chris Tabor',
    maintainer_email='dxdstudio@gmail.com',
    url='https://github.com/christabor/csscms',
    keywords=keywords,
    license='Apache License 2.0',
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=_get_requires('requirements.txt'),
    setup_requires=[
        'setuptools>=0.8',
    ],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Text Processing',
        'Topic :: Utilities',
    ]
)

#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'MM'
SITENAME = 'Magda Mozgawa'
SITESUBTITLE = 'personal site'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Warsaw'

DEFAULT_LANG = 'en'

THEME = "/home/mkay313/Projects/magda_space/venv/lib/python3.7/site-packages/pelican/themes/pelican-left"

# Feed generation is usually not desired when developing
FEED_RSS = None

# Social widget
# SOCIAL = (('You can add links in your config file', '#'),
#           ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Display the blog post date and summary on the index page

HIDE_DATE = True 
HIDE_SUMMARY = True

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

MARKUP = ('md', 'ipynb')

PLUGIN_PATHS = ['./plugins']
PLUGINS = ['ipynb.markup']

IGNORE_FILES = ['.ipynb_checkpoints']

STATIC_PATHS = ['extra/CNAME']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}

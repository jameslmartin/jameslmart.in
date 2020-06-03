#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'james'
SITENAME = 'jameslmart.in'
SITEURL = 'http://localhost:8000'
SITESUBTITLE = 'researcher, engineer, community advocate'

THEME = '/home/themes/mod'

ARTICLE_URL = ('{slug}/')
ARTICLE_SAVE_AS = ('{slug}/index.html')
PAGE_URL = ('{slug}/')
PAGE_SAVE_AS = ('{slug}/index.html')
AUTHOR_URL = ('author/{name}/')
AUTHOR_SAVE_AS = ('author/{name}/index.html')
TAG_URL = ('tag/{name}/')

PATH = 'content'
OUTPUT_PATH = 'public'
STATIC_PATHS = ['images', 'extra/CNAME']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}
PLUGIN_PATHS = ['/home/plugins']
PLUGINS = ['dither','addressable_paragraphs']

TIMEZONE = 'America/New_York'

DEFAULT_LANG = 'en'

USE_FOLDER_AS_CATEGORY = True
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False

# For dev
DELETE_OUTPUT_DIRECTORY = True

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Plugins
THRESHOLD = [96, 96, 96]
TRANSPARENCY = True
RESIZE_OUTPUT = False
#MAX_SIZE = (800, 800)
DITHER_PALETTE = [(25,25,25),(75,75,75),(125,125,125),(175,175,175),(225,225,225),(250,250,250)]

# Blogroll
LINKS = (('GitHub', 'https://github.com/jameslmartin'),
         ('Keybase', 'https://keybase.io/jlmartin'),
         ('Instagram', 'https://www.instagram.com/jameslmartin/'),
         ('LinkedIn', 'https://www.linkedin.com/in/jamesloganmartin/'))


DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

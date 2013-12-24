#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Arnaud TANGUY'
SITENAME = 'VIM Proves The World'
SITEURL = ''

#THEME = "themes/bootstrap2"
THEME = "themes/tuxlite_tbs"


TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Afnarel', 'http://afnarel.com/'),
          ('Pelican', 'http://getpelican.com/'),
          ('Python.org', 'http://python.org/'),
          ('You can modify those links in your config file', '#'))

# Social widget
SOCIAL = (('LinkedIn', 'http://www.linkedin.com/pub/arnaud-tanguy/34/a69/6a6'),
          ('Twitter', 'https://twitter.com/arntanguy'),
          ('Github', 'https://github.com/geenux'),
          ('Bitbucket', 'https://bitbucket.org/arn_tanguy'),
          ('Google+', 'https://plus.google.com/u/0/+ArnaudTanguy29'))

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True



###############################################################################
##################    Custom Settings      ####################################
###############################################################################
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
DEFAULT_DATE = 'fs'
THEME = 'themes/elegant'
TWITTER_USERNAME = 'arntanguy'

# specific to Elegant theme:
# http://oncrashreboot.com/elegant-a-clean-theme-for-pelican-with-search-feature
PLUGIN_PATH = 'plugins'
# Plugins:
#- Latex plugin uses MathJaX
PLUGINS = ['sitemap', 'extract_toc', 'tipue_search', 'latex']
MD_EXTENSIONS = ['codehilite(css_class=highlight)', 'extra', 'headerid', 'toc']
STATIC_PATHS = ['theme/images', 'images', 'download']
DIRECT_TEMPLATES = (('index', 'tags', 'categories','archives',
                     'search', '404'))
TAG_SAVE_AS = ''
CATEGORY_SAVE_AS = ''
AUTHOR_SAVE_AS = ''

###########
# Home page
###########
LANDING_PAGE_ABOUT={'title' : 'Computer Graphics, Vision, Augmented Reality',
                    'details' : """My name is Arnaud TANGUY, I am currently doing a Computer
                    Science master at Polytech' Nice-Sophia.
                    I am mostly interested in real-time rendering, real-time physics
                    and augmented reality, and hopefully you'll be seeing a lot of those
                    in this blog.
                    In 2012, I studied abroad at Trinity College Dublin. You'll see
                    some of my projects written during this year (a simple
                    physics engine along with some rendering projects).

                    This blog will hopefully show you some of my projects, and
                    might even be helpful, who knows ;)
                    """ }

PROJECTS=[{'name': 'FotoWall', 'url' :
'http://enricoros.com/opensource/fotowall', 'description' : """Fotowall is an
opensource creative tool that lets you play with your pixels as you've ever
wanted! Make the perfect arrangement with your photos, add text, live video
from your webcam and the best internet pictures."""},
{'name': 'Computer Graphics', 'url' :
'http://www.youtube.com/playlist?list=PLJj-ZhCpFn7Eywrbt5YW9ZCxgs4Jux0Bs',
'description' : """Videos of my real-time physics and rendering projects made during my year at
 Trinity College Dublin"""},
{'name': 'CGEngine', 'url' : '',
'description' : """A simple OpenGL C++ rendering engine that I developped and
use in my various projects"""},
{'name': 'PHEngine', 'url' : '',
'description' : """A simple OpenGL C++ physics engine that I developped during my year at TCD"""}
]

RECENT_ARTICLES_COUNT=15


########### COMMENTS
COMMENTS_INTRO="""So what do you think? Did I miss something? Is any part
unclear? Leave your comments below."""
DISQUS_SITENAME="geenux"

### GOOGLE
GOOGLE_ANALYTICS="UA-46439484-1"

# Appears before the licence and after site name
SITESUBTITLE=""
SITE_LICENSE = '''<a rel="license"
href="http://creativecommons.org/licenses/by-sa/3.0/"><img
alt="Creative Commons License" style="border-width:0"
src="http://i.creativecommons.org/l/by-sa/3.0/80x15.png" /></a><br
/>This work is licensed under a <a rel="license"
href="http://creativecommons.org/licenses/by-sa/3.0/">Creative Commons
Attribution-ShareAlike 3.0 Unported License</a>.'''

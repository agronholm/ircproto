#!/usr/bin/env python
# coding: utf-8
import pkg_resources

extensions = [
    'sphinx.ext.autodoc',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'ircproto'
author = u'Alex Grönholm'
copyright = '2016, ' + author

v = pkg_resources.get_distribution('ircproto').parsed_version
version = v.base_version
release = v.public

language = None

exclude_patterns = ['_build']
pygments_style = 'sphinx'
todo_include_todos = False

html_theme = 'classic'
html_static_path = ['_static']
htmlhelp_basename = 'ircprotodoc'

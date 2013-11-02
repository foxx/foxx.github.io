#!/usr/bin/env python
# -*- coding: utf-8 -*-
from jinja2 import Environment, PackageLoader, Template
from bottle import route, run, template

import os
import markdown

class ContentBuilder(object):
    def __init__(self):
        self.env = Environment(loader=PackageLoader('contentbuilder', ))

    def fetch_articles(self):
        articles = []
        for article_filename in os.listdir("contentbuilder/templates/articles/"):
            article = dict()
            article['template_path'] = "articles/%s" % ( article_filename, )
            article['template'] = self.env.get_template(article['template_path'])
            article['title'] = ''.join(article['template'].blocks['title']({})).strip()
            article['content'] = ''.join(article['template'].blocks['content']({})).strip()
            article['content_html'] = markdown.markdown(article['content'])
            articles.append(article)
        return articles

    def build(self):
        # Build index page
        articles = self.fetch_articles()
        opts = dict(articles=articles)
        print self.env.get_template('home.html').render(opts)

def runserver():
    pass

if __name__ == '__main__':
    runserver()

cb = ContentBuilder()
cb.build()

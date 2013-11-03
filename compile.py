#!/usr/bin/env python
# -*- coding: utf-8 -*-
from jinja2 import Environment, PackageLoader, Template
from bottle import route, run, template

import os
import markdown
import socket

LISTEN_ADDR = '0.0.0.0'
LISTEN_PORT = 8080

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
            article['name'] = os.path.splitext(article_filename)[0]
            articles.append(article)
        return articles

    def build(self):
        # Build index page
        articles = self.fetch_articles()
        opts = dict(articles=articles)
        print self.env.get_template('home.html').render(opts)

def runserver():
    """
    Emulate how github pages works, allows local preview etc
    """

    @route('/<filename>')
    def index(filename=None):
        return "WTF"
        #return template('<b>Hello {{name}}</b>!', name=name)
    print "Running on http://%s:%s" % ( socket.gethostname(), LISTEN_PORT, )
    run(host=LISTEN_ADDR, port=LISTEN_PORT)

    

if __name__ == '__main__':
    from bottle import route, run, template
    runserver()

#cb = ContentBuilder()
#cb.build()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from jinja2 import Environment, PackageLoader, Template
from bottle import route, run, template

import os
import markdown
import socket
import shutil
import scss

LISTEN_ADDR = '0.0.0.0'
LISTEN_PORT = 8080

def get_project_root(path=None):
    base = os.path.dirname(os.path.abspath(__file__))
    path = "%s/%s" % ( base, path, ) if path else base
    PROJECT_ROOT = os.path.realpath(path)
    return PROJECT_ROOT

class ContentBuilder(object):
    SCSS_ROOT = get_project_root("contentbuilder/static/scss/")
    SCSS_OUTPUT_ROOT = get_project_root("blog/static/scss/")
    STATIC_ROOT = get_project_root("contentbuilder/static/")
    STATIC_OUTPUT_ROOT = get_project_root("blog/static/")

    def __init__(self):
        self.env = Environment(loader=PackageLoader('contentbuilder', ))
        self.prep_scss()

    def prep_scss(self):
        from scss import Scss
        _scss = Scss(search_paths=(self.SCSS_ROOT, ))
        self.scss = _scss

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
        def write_to_file(path, content):
            with open(path, 'wb') as fd:
                fd.write(content.encode('utf-8'))

        # clear out old static
        output_root = get_project_root("blog/")
        if os.path.exists(output_root):
            shutil.rmtree(output_root)

        if not os.path.exists(output_root):
            os.mkdir(output_root)

        # copy static
        #os.makedirs(self.SCSS_OUTPUT_ROOT, )
        #os.makedirs(self.STATIC_OUTPUT_ROOT)
        shutil.copytree(self.STATIC_ROOT, self.STATIC_OUTPUT_ROOT)

        # temp assign
        articles = self.fetch_articles()
        opts = dict(articles=articles)

        # build blog index page
        index_path = get_project_root("blog/home.html")
        index_content = self.env.get_template('home.html').render(opts)
        write_to_file(index_path, index_content)

        # build scss
        css = ""
        for fn in os.listdir(self.SCSS_ROOT):
            filename, ext = os.path.splitext(fn)
            if fn.startswith("_"):
                continue
            path = "%s/%s" % ( self.SCSS_ROOT, fn, )
            output = self.scss.compile(scss_file=path)
            outpath = "%s/%s.css" % ( self.SCSS_OUTPUT_ROOT, filename, )
            write_to_file(outpath, output)

def runserver():
    """
    Emulate how github pages works, allows local preview etc
    """

    @route("/<url:re:.+|>")
    def index(url):
        cb = ContentBuilder()
        cb.build()
        url = "/%s" % ( url, ) if url else "/index"
        has_ext = True if os.path.splitext(os.path.basename(url))[1] else False
        url = "%s.html" % ( url, ) if not has_ext else url
        
        target_file = get_project_root("/%s" % ( url, ))

        return template('<b>Hello {{target_file}}</b>!', target_file=target_file)

    print "Running on http://%s:%s" % ( socket.gethostname(), LISTEN_PORT, )
    run(host=LISTEN_ADDR, port=LISTEN_PORT, reloader=True)


if __name__ == '__main__':
    from bottle import route, run, template
    runserver()



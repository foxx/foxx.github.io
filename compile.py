#!/usr/bin/env python
# -*- coding: utf-8 -*-
from jinja2 import Environment, PackageLoader, Template
from bottle import route, run, template, static_file

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
    SCSS_OUTPUT_ROOT = get_project_root("static/scss/")
    STATIC_ROOT = get_project_root("contentbuilder/static/")
    STATIC_OUTPUT_ROOT = get_project_root("static/")

    def __init__(self):
        self.env = Environment(loader=PackageLoader('contentbuilder', ))
        self.prep_scss()

    def prep_scss(self):
        from scss import Scss
        _scss = Scss(search_paths=(self.SCSS_ROOT, ))
        self.scss = _scss

    def fetch_articles(self):
        articles = []

        files = os.listdir("contentbuilder/templates/articles/")
        def fsort(v,):
            v = int(v.split("-")[0])
            return v

        files = sorted(files, key=fsort)
        files = reversed(files)

        for article_filename in files:
            article = dict()
            article['template_path'] = "articles/%s" % ( article_filename, )
            article['template'] = self.env.get_template(article['template_path'])
            article['title'] = ''.join(article['template'].blocks['title']({})).strip()
            article['content'] = ''.join(article['template'].blocks['content']({})).strip()
            article['content_html'] = markdown.markdown(article['content'])
            article['content_excerpt'] = markdown.markdown(article['content'].strip().split("\n")[0])
            article['coverimage'] = ''.join(article['template'].blocks['coverimage']({})).strip()
            article['name'] = os.path.splitext(article_filename)[0]
            articles.append(article)
        return articles

    def build(self):
        def write_to_file(path, content):
            with open(path, 'wb') as fd:
                fd.write(content.encode('utf-8'))

        def remove_if_exists(path):
            if os.path.exists(path):
                shutil.rmtree(path)

        def create_if_not_exists(path):
            if not os.path.exists(path):
                os.makedirs(path)

        # clear out old static
        remove_if_exists(get_project_root("blog/"))
        remove_if_exists(self.STATIC_OUTPUT_ROOT)

        create_if_not_exists(get_project_root("blog/"))

        # copy static
        shutil.copytree(self.STATIC_ROOT, self.STATIC_OUTPUT_ROOT)

        # temp assign
        articles = self.fetch_articles()
        opts = dict(articles=articles)

        # build blog index page
        home_path = get_project_root("index.html")
        index_path = get_project_root("blog/index.html")
        index_content = self.env.get_template('home.html').render(opts)
        write_to_file(index_path, index_content)
        write_to_file(home_path, index_content)

        # compile 404
        path_404 = get_project_root("404.html")
        content_404 = self.env.get_template('404.html').render(opts)
        write_to_file(path_404, content_404)

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

        url = url if url else "index.html"
        target_path = "/%s" % ( url, )
        target_path_full = get_project_root(target_path)

        if not os.path.exists(target_path_full):
            target_file = "/404.html"
        elif os.path.isdir(target_path_full):
            target_file = "%s/index.html" % ( target_path, )
        else:
            target_file = target_path

        return static_file(target_file, get_project_root())

    print "Running on http://%s:%s" % ( socket.gethostname(), LISTEN_PORT, )
    run(host=LISTEN_ADDR, port=LISTEN_PORT, reloader=True)


if __name__ == '__main__':
    runserver()
    #cb = ContentBuilder()
    #cb.build()

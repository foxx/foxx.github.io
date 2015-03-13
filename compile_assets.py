#!/usr/bin/env python

from base64 import b64encode
import fnmatch
import os

# Quick hack for embedding images in CSS
# Yeah, I know it's nasty

FONT_SASS_TMPL = """@font-face{ font-family: "%(font_name)s"; src: url(data:application/x-font-woff;base64,%(b64data)s); font-weight:300; font-style:normal; } """
FONT_OUTPUT_FILE = '_sass/site/fonts.scss'

IMAGE_SASS_TMPL = """.img-%(image_name)s { background-image: url(data:application/png;base64,%(b64data)s); } """
IMAGE_OUTPUT_FILE = '_sass/site/images.scss'

def recursive_glob(path, pattern='*'):
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, pattern):
            yield os.path.join(root, filename)

def compile_fonts():
    out = ""
    for font_path in recursive_glob("./fonts", '*.woff'):
        data = {}
        data['font_name'] = os.path.splitext(os.path.basename(font_path))[0]
        with open(font_path, 'rb') as fh:
            data['b64data'] = b64encode(fh.read())
        out += FONT_SASS_TMPL % data
        out += "\n"

    with open(FONT_OUTPUT_FILE, 'wb') as fh:
        fh.write(out)

def compile_images():
    out = ""
    for path in recursive_glob("./img/social", '*.png'):
        data = {}
        data['image_name'] = os.path.splitext(os.path.basename(path))[0]
        with open(path, 'rb') as fh:
            data['b64data'] = b64encode(fh.read())
        out += IMAGE_SASS_TMPL % data
        out += "\n"

    with open(IMAGE_OUTPUT_FILE, 'wb') as fh:
        fh.write(out)    


if __name__ == '__main__':
    compile_fonts()
    compile_images()

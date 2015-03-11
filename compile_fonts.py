#!/usr/bin/env python

from glob import glob
from base64 import b64encode

import os

SASS_TMPL = """@font-face{ font-family: "%(font_name)s"; src: url(data:application/x-font-woff;base64,%(woff_data)s); font-weight:300; font-style:normal; } """
OUTPUT_FILE = 'css/fonts.css'

def compile():
    out = ""
    for font_path in glob("./fonts/*.woff"):
        data = {}
        data['font_name'] = os.path.splitext(os.path.basename(font_path))[0]
        with open(font_path, 'rb') as fh:
            data['woff_data'] = b64encode(fh.read())
        out += SASS_TMPL % data
        out += "\n"

    with open(OUTPUT_FILE, 'wb') as fh:
        fh.write(out)


if __name__ == '__main__':
    compile()
    #@font-face{ font-family: "Gotham Narrow SSm A"; src: url(data:application/x-font-woff;base64,XXX); font-weight:300; font-style:normal; } 
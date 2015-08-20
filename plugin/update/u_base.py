# -*- coding: utf-8 -*-
# u_base.py for lieying_plugin/module-update (plugin)
# plugin/update/u_base: update base function, import py-htmldom from sub
# version 0.0.2.0 test201508071432

# import

from .. import sub

# global vars

# function
def create_dom(html_text):
    dom = htmldom.HtmlDom()
    root = dom.createDom(html_text)
    return root

# import py-htmldom now

htmldom = sub.get_htmldom()

# end u_base.py



# -*- coding: utf-8 -*-
# base.py for lieying_plugin update
# o/update/base: update base utils
# version 0.0.1.1 test201507262258

# import

import os
import sys

# global vars
ROOT_PATH = '../../'

# base function
def make_root_path():
    now_path = os.path.dirname(__file__)
    root_path = os.path.join(now_path, ROOT_PATH)
    
    return root_path

# function
def create_dom(html_text):
    return base0.create_dom(html_text)

# import TOO

# NOTE import base from plugin/plist
root_path = make_root_path()
sys.path.append(root_path)

from plugin.plist import base as base0

# end base.py



# -*- coding: utf-8 -*-
# main.py for lieying_plugin/you-get (parse)
# plugin/main: plugin main file. 
# version 0.0.3.0 test201507131141

# import

import json

from . import version
from . import filter as filter0

from . import conf
from . import tinfo
from . import run_sub

from .plist import entry as plist

from . import parse_you_get as parse0

# function

# parse one video
def parse_one(url):
    pass

# parse more video
def parse_more(url):
    pass

# lieying_plugin functions

def lieying_plugin_GetVersion():
    out = {}	# output info obj
    
    out['port_version'] = version.LIEYING_PLUGIN_PORT_VERSION
    out['type'] = version.LIEYING_PLUGIN_TYPE
    out['uuid'] = version.LIEYING_PLUGIN_UUID
    out['version'] = version.LIEYING_PLUGIN_VERSION
    
    out['name'] = version.make_plugin_name()
    out['filter'] = filter0.get_filter()
    
    out['author'] = version.THIS_AUTHOR
    out['license'] = version.THIS_LICENSE
    out['home'] = version.THIS_HOME
    out['note'] = version.THIS_NOTE
    
    # self define info
    out['pack_version'] = version.THIS_PACK_VERSION
    
    # done
    text = json.dumps(out)
    return text

def lieying_plugin_StartConfig():
    raise Exception('lieying_plugin/you-get: ERROR: [StartConfig()] not support config now. ')

def lieying_plugin_Parse(input_text):
    pass

def lieying_plugin_ParseURL(url, label, i_min=None, i_max=None):
    pass

# end main.py



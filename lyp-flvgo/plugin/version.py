# -*- coding: utf-8 -*-
# version.py for lieying_plugin/flvgo (parse)
# plugin/version: define info for GetVersion()
# version 0.0.9.0 test201507161233

# import
from . import conf

# global vars

THIS_PACK_VERSION = '4'

LIEYING_PLUGIN_PORT_VERSION = '0.2.1'
LIEYING_PLUGIN_TYPE = 'parse'

LIEYING_PLUGIN_UUID = 'e536174b-7d87-4fa0-9d7e-f068fcab169e'
LIEYING_PLUGIN_VERSION = '0.3.0'

THIS_AUTHOR = 'sceext <sceext@foxmail.com>'
THIS_LICENSE = 'unlicense <http://unlicense.org> and FreeBSD License'
THIS_HOME = 'https://github.com/sceext2/lieying_plugin/tree/plugin-flvgo'
THIS_NOTE = 'A lieying plugin (parse) with parse support of flvgo <http://flvgo.com/>. '

THIS_RAW_NAME = [
    'lieying_plugin_flvgo ', 
    ' (plugin version ', 
    ') ', 
]

# function

# make plugin name
def make_plugin_name():
    name = ''	# plugin name
    raw = THIS_RAW_NAME
    
    name += raw[0] + THIS_PACK_VERSION
    name += raw[1] + LIEYING_PLUGIN_VERSION + raw[2]
    
    name += THIS_LICENSE
    
    # done
    return name

# end version.py



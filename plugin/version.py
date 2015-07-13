# -*- coding: utf-8 -*-
# version.py for lieying_plugin/you-get (parse)
# plugin/version: define info for GetVersion()
# version 0.0.2.0 test201507131133

# import
from . import conf
from . import run_sub

# global vars

THIS_PACK_VERSION = '1'

LIEYING_PLUGIN_PORT_VERSION = '0.2.0'
LIEYING_PLUGIN_TYPE = 'parse'

LIEYING_PLUGIN_UUID = '588e29b8-cc31-4416-9ed7-80b48f7971a1'
LIEYING_PLUGIN_VERSION = '0.0.1'

THIS_AUTHOR = 'sceext <sceext@foxmail.com>'
THIS_LICENSE = 'unlicense <http://unlicense.org> and FreeBSD License'
THIS_HOME = 'https://github.com/sceext2/lieying_plugin/tree/plugin-you-get'
THIS_NOTE = 'A lieying plugin (parse) with parse support of you-get <https://github.com/soimort/you-get>. '

THIS_RAW_NAME = [
    'lieying_plugin_you-get', 
    ' (plugin version ', 
    ', you-get version ', 
    ') ', 
]

# function

# get you-get version
def get_you_get_version():
    # TODO not finished
    return '[unknow]'

# make plugin name
def make_plugin_name():
    name = ''	# plugin name
    raw = THIS_RAW_NAME
    
    name += raw[0] + THIS_PACK_VERSION
    name += raw[1] + LIEYING_PLUGIN_VERSION
    name += raw[2] + get_you_get_version() + raw[3]
    
    name += THIS_LICENSE
    
    # done
    return name

# end version.py



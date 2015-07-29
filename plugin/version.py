# -*- coding: utf-8 -*-
# version.py for lieying_plugin/module-py-htmldom (plugin)
# plugin/version: define info for GetVersion()
# version 0.1.0.0 test201507291815

# global vars

THIS_PACK_VERSION = '2'
HTMLDOM_VERSION = '2.0'

LIEYING_PLUGIN_PORT_VERSION = '0.3.0-test.5'
LIEYING_PLUGIN_TYPE = 'plugin'

LIEYING_PLUGIN_UUID = '9c446d5b-7e55-479a-9afa-a53d251c3f7f'
LIEYING_PLUGIN_VERSION = '0.1.0'

THIS_AUTHOR = 'sceext <sceext@foxmail.com>'
THIS_LICENSE = 'unlicense <http://unlicense.org> and FreeBSD License'
THIS_HOME = 'https://github.com/sceext2/lieying_plugin/tree/module-py-htmldom'
THIS_NOTE = 'A lieying plugin (plugin) to support py-htmldom functions to other plugins. '

THIS_RAW_NAME = [
    'plugin/module-py-htmldom [sceext] ', 
    ' (plugin version ', 
    ') ', 
]

# function

# make plugin name
def make_plugin_name():
    name = ''	# plugin name
    raw = THIS_RAW_NAME
    
    name += raw[0] + THIS_PACK_VERSION
    name += raw[1] + LIEYING_PLUGIN_VERSION
    name += raw[2]
    
    name += THIS_LICENSE
    
    # done
    return name

# end version.py



# -*- coding: utf-8 -*-
# version.py for lieying_plugin/module-update (plugin)
# plugin/version: define info for GetVersion()
# version 0.0.2.0 test201508041606

# global vars

THIS_PACK_VERSION = '1'
UPDATE_TOOL_VERSION = '0.1.0'

LIEYING_PLUGIN_PORT_VERSION = '0.3.0-test.5'
LIEYING_PLUGIN_TYPE = 'plugin'

LIEYING_PLUGIN_UUID = 'eb3c4bab-5360-4c55-b915-31d8a4e4690f'
LIEYING_PLUGIN_VERSION = '0.1.0'

THIS_AUTHOR = 'sceext <sceext@foxmail.com>'
THIS_LICENSE = 'unlicense <http://unlicense.org>'
THIS_HOME = 'https://github.com/sceext2/lieying_plugin/tree/module-update'
THIS_NOTE = 'A lieying plugin (plugin) to support update functions to other plugins. '

THIS_RAW_NAME = [
    'plugin/module-update [sceext] ', 
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

# get uuid
def get_uuid():
    return LIEYING_PLUGIN_UUID

# end version.py



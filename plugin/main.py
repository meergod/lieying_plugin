# -*- coding: utf-8 -*-
# main.py for lieying_plugin/module-py-htmldom (plugin)
# plugin/main: plugin main file. 
# version 0.0.1.0 test201507291810

# import

import json

from . import version
from .tool.htmldom import htmldom

# global vars

# function

# functions to export by this module
def get_htmldom():
    return htmldom

# lieying_plugin functions

def lieying_plugin_GetVersion():
    
    out = {
        'port_version' : version.LIEYING_PLUGIN_PORT_VERSION, 
        'type' : version.LIEYING_PLUGIN_TYPE, 
        'uuid' : version.LIEYING_PLUGIN_UUID, 
        'version' : version.LIEYING_PLUGIN_VERSION, 
        
        'author' : version.THIS_AUTHOR, 
        'license' : version.THIS_LICENSE, 
        'home' : version.THIS_HOME, 
        'note' : version.THIS_NOTE, 
        
        # self define info
        'pack_version' : version.THIS_PACK_VERSION, 
        'htmldom_version' : version.HTMLDOM_VERSION, 
    }	# output info obj
    
    out['name'] = version.make_plugin_name()
    
    # done
    text = json.dumps(out)
    return text

def lieying_plugin_StartConfig():
    raise Exception('lieying_plugin/module-py-htmldom: ERROR: [StartConfig()] not support now')

def lieying_plugin_Update(local_path=''):
    raise Exception('lieying_plugin/module-py-htmldom: ERROR: [Update()] not support now')

# end main.py



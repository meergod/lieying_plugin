# -*- coding: utf-8 -*-
<<<<<<< HEAD
# main.py for lieying_plugin/module-py-htmldom (plugin)
# plugin/main: plugin main file. 
# version 0.0.1.0 test201507291810
=======
# main.py for lieying_plugin/module-update (plugin)
# plugin/main: plugin main file. 
# version 0.0.0.1 test201507301803
>>>>>>> module-update

# import

import json

from . import version
<<<<<<< HEAD
from .tool.htmldom import htmldom
=======
from . import sub
>>>>>>> module-update

# global vars

# function

# functions to export by this module
<<<<<<< HEAD
def get_htmldom():
    return htmldom
=======

# module-update functions

# easy update function, just offer uuid and config, then hook its plugin update function to this. 
def easy_update(local_path='', plugin_uuid=None, conf=None):
    pass

>>>>>>> module-update

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
<<<<<<< HEAD
        'htmldom_version' : version.HTMLDOM_VERSION, 
=======
        'update_tool_version' : version.UPDATE_TOOL_VERSION, 
>>>>>>> module-update
    }	# output info obj
    
    out['name'] = version.make_plugin_name()
    
    # done
    text = json.dumps(out)
    return text    

def lieying_plugin_StartConfig():
<<<<<<< HEAD
    raise Exception('lieying_plugin/module-py-htmldom: ERROR: [StartConfig()] not support now')

def lieying_plugin_Update(local_path=''):
    raise Exception('lieying_plugin/module-py-htmldom: ERROR: [Update()] not support now')
=======
    raise Exception('lieying_plugin/module-update: ERROR: [StartConfig()] not support now')

def lieying_plugin_Update(local_path=''):
    # TODO
    # check local_path for network update or local update
    if local_path == '':
        zip_file = update.update_network()
        return zip_file
    else:	# should update from local
        return update.update_local(local_path)
    # update done
>>>>>>> module-update

# end main.py



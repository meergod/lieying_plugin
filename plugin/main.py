# -*- coding: utf-8 -*-
# main.py for lieying_plugin/module-update (plugin)
# plugin/main: plugin main file. 
# version 0.0.1.0 test201508041710

# import

import os
import json

from . import version
from . import sub
from .tool import update as update0

# global vars

LOCAL_UPDATE_CONFIG_FILE = 'o/update_config.json'

# function

# functions to export by this module

# module-update functions

# easy update function, just offer uuid and config, then hook its plugin update function to this. 
def easy_update(local_path='', plugin_uuid=None, conf=None):
    # TODO
    # check local_path for network update or local update
    if local_path == '':
        zip_file = update.update_network()
        return zip_file
    else:	# should update from local
        return update.update_local(local_path)
    # update done
    pass	# TODO

# update local
def update_local(local_path='', plugin_uuid=None, conf=None):
    pass	# TODO

# update network
def update_network(plugin_uuid=None, conf=None):
    pass	# TODO


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
        'update_tool_version' : version.UPDATE_TOOL_VERSION, 
    }	# output info obj
    
    out['name'] = version.make_plugin_name()
    
    # done
    text = json.dumps(out)
    return text    

def lieying_plugin_StartConfig():
    raise Exception('lieying_plugin/module-update: ERROR: [StartConfig()] not support now')

def lieying_plugin_Update(local_path=''):
    # get update_config file path
    root_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../'))
    update_conf_file = os.path.join(root_path, LOCAL_UPDATE_CONFIG_FILE)
    
    # NOTE fix for lieying_plugin/module-update
    # try to import py-htmldom
    flag_skip = False
    try:
        htmldom = sub.get_sub('htmldom')
    except Exception:
        flag_skip = True
    
    # just use common update function
    result = update0.do_update(local_path=local_path, local_config_file=update_conf_file, flag_skip_update_this=flag_skip)
    return result	# done

# end main.py



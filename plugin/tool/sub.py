# -*- coding: utf-8 -*-
# sub.py for lieying_plugin [sceext] plugin/tool, common tools
# plugin/tool/sub: get and use sub modules
# version 0.0.1.0 test201508041630

# import

import importlib

# global vars

etc = {}	# global config info obj
etc['loaded_list'] = {}	# imported sub list, to prevent re-import

# base function

# convert plugin uuid to plugin root_dir name
def uuid2root_dir(uuid_str):
    root_dir = '_' + uuid_str.replace('-', '_')
    return root_dir

def import_sub(root_dir):
    # from _<uuid> import run
    sub = importlib.__import__(root_dir, globals(), locals(), ['run'], 0)
    run = sub.run
    # import done
    return run

# function

# raw get_sub function, just import sub, with check loaded_list, nothing more
def raw_get_sub(sub_name, sub_list={}, flag_debug=True):
    # check loaded list
    if sub_name in etc['loaded_list']:
        sub = etc['loaded_list'][sub_name]
    else:
        # do import
        sub_uuid = sub_list[sub_name][0]
        sub_root_dir = uuid2root_dir(sub_uuid)
        
        # print for DEBUG
        if flag_debug:
            print('plugin.tool.sub :: DEBUG: import [' + sub_name + '] (uuid ' + sub_uuid + ') ')
        
        sub = import_sub(sub_root_dir)
        # add to loaded list
        etc['loaded_list'][sub_name] = sub
    # done
    return sub

# get_sub, used in normal module, if failed, raise a Exception for user to read
def get_sub(sub_name, sub_list={}):
    
    # try to get_sub
    try:
        sub = raw_get_sub(sub_name, sub_list)
        return sub	# successfully finished
    except Exception as e:	# import error
        # get sub info
        sub_item = sub_list[sub_name]
        sub_uuid = sub_item[0]
        # print for DEBUG
        print('plugin.tool.sub :: DEBUG: get_sub() raw failed, sub_name [' + sub_name + '] uuid [' + sub_uuid + '] ')
        print(e)
        # raise new Exception
        err_text = 'plugin.tool.sub :: ERROR: import sub [' + sub_name + '] uuid [' + sub_uuid + '] failed \n'
        err_text += '    please Update this plugin, or install the module manually. \n'
        raise Exception(err_text, e)
    # done

# end sub.py



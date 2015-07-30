# -*- coding: utf-8 -*-
# sub.py for lieying_plugin/module-update (plugin)
# plugin/sub: sub module process. 
# version 0.0.1.0 test201507301749

# import

import importlib

# global vars

# sub module list, used by this plugin
SUB_MODULE_LIST = {
    'htmldom' : [	# lieying_plugin/module-py-htmldom
        '9c446d5b-7e55-479a-9afa-a53d251c3f7f', 
        'https://github.com/sceext2/lieying_plugin/archive/module-py-htmldom.zip', 
    ], 
}

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

# common function

# import and return sub module by sub_name in SUB_MODULE_LIST
def get_sub(sub_name):
    # check loaded list
    if sub_name in etc['loaded_list']:
        return etc['loaded_list'][sub_name]
    
    # do import
    sub_list = SUB_MODULE_LIST
    sub_uuid = sub_list[sub_name][0]
    sub_root_dir = uuid2root_dir(sub_uuid)
    
    # print for DEBUG
    print('plugin.sub :: DEBUG: import [' + sub_name + '] (uuid ' + sub_uuid + ') ')
    
    sub = import_sub(sub_root_dir)
    # add to loaded list
    etc['loaded_list'][sub_name] = sub
    # done
    return sub

# check sub module, try to import for update
def check_sub4update():
    sub_list = SUB_MODULE_LIST
    # try to import each sub
    for s in sub_list:
        sub_uuid = sub_list[s][0]
        try:	# try to import this sub
            get_sub(s)
        except Exception as e:
            # print for debug
            print('plugin.sub :: ERROR: import [' + s + '] (uuid ' + sub_uuid + ') failed, ' + str(e))
            # get this sub download url
            sub_url = sub_list[s][1]
            print('plugin.sub :: INFO: got [' + s + '] download URL \"' + sub_url + '\" ')
            # will auto install this sub
            return sub_url
    # check sub done
    return ''	# no more to do

# plugin self function

# get core from module-py-htmldom
def get_htmldom():
    sub = get_sub('htmldom')
    dom = sub.get_htmldom()
    return dom

# end sub.py



# -*- coding: utf-8 -*-
# sub.py for lieying_plugin/module-update
# plugin/sub: this plugin sub data
# version 0.0.2.0 test201508041643

# import

from .tool import sub

# global vars

# sub module list, used by this plugin
SUB_MODULE_LIST = {
    'htmldom' : [	# lieying_plugin/module-py-htmldom
        '9c446d5b-7e55-479a-9afa-a53d251c3f7f', 
        'https://github.com/sceext2/lieying_plugin/archive/module-py-htmldom.zip', 
    ], 
    'update' : [	# lieying_plugin/module-update
        'eb3c4bab-5360-4c55-b915-31d8a4e4690f', 
        'https://github.com/sceext2/lieying_plugin/archive/module-update.zip', 
    ], 
}

# function

# import and get_sub
def get_sub(sub_name):
    # just use tool.sub
    return sub.get_sub(sub_name, SUB_MODULE_LIST)

# this plugin sub function

# get core from module-py-htmldom
def get_htmldom():
    sub = get_sub('htmldom')
    dom = sub.get_htmldom()
    return dom

# export sub_list
def get_sub_list():
    return SUB_MODULE_LIST

# end sub.py



# -*- coding: utf-8 -*-
# update.py for lieying_plugin [sceext] plugin/tool, common tools
# plugin/tool/update: common support Update() function
# version 0.0.2.0 test201508041657

# import

import json

from .. import version
from .. import sub

# global vars

# functions

# just call this update function in exports Update() function
def do_update(local_path='', local_config_file=None, flag_skip_update_this=False):
    
    # get this uuid
    this_uuid = version.get_uuid()
    
    # try to import module-update
    try:
        m_update = sub.get_sub('update')
    except Exception as e:
        # get update module info
        sub_item = sub.get_sub_list()['update']
        sub_uuid = sub_item[0]
        sub_url = sub_item[1]
        # print for DEBUG
        print('plugin.tool.update :: ERROR: import [update] sub module failed, (uuid ' + sub_uuid + ') ')
        print('plugin.tool.update :: INFO: ready to download [update] from \"' + sub_url + '\" ')
        # just return sub_url
        return sub_url
    # continue update
    
    # load config file
    with open(local_config_file) as f:
        raw_text = f.read()
    update_conf = json.loads(raw_text)
    
    # NOTE update this, use common lieying_plugin/module-update
    if not flag_skip_update_this:
        result = m_update.easy_update(local_path=local_path, conf=update_conf, plugin_uuid=this_uuid)
        # check update result
        if result != '':
            return result	# should re-install this plugin
    
    # check sub_modules
    result = check_sub4update()
    return result	# update done

# check sub module, try to import for update
def check_sub4update():
    # get sub_list from ..sub
    sub_list = sub.get_sub_list()
    # try to import each sub
    for sub_name in sub_list:
        sub_item = sub_list[sub_name]
        sub_uuid = sub_item[0]
        try:	# try to import this sub
            sub.raw_get_sub(sub_name, flag_debug=False)
        except Exception as e:
            # print for debug
            print('plugin.tool.update :: ERROR: import [' + sub_name + '] (uuid ' + sub_uuid + ') failed, ' + str(e))
            # get this sub download url
            sub_url = sub_item[1]
            print('plugin.tool.update :: INFO: got [' + sub_name + '] download URL \"' + sub_url + '\" ')
            # will auto install this sub
            return sub_url
    # check sub done
    return ''	# no more to do


# end update.py



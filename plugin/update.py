# -*- coding: utf-8 -*-
# update.py for lieying_plugin/youtube-dl (parse)
# plugin/update: plugin update function. 
# version 0.0.3.0 test201507281430

# import

import os
import sys
import json

from . import run_sub
from .plist import base

# global vars
etc = {}	# global config info obj

etc['to_root_path'] = '../'
etc['update_conf'] = 'etc/update_config.json'
etc['bin_update_plugin'] = 'o/update_plugin.py'
etc['bin_update_sub'] = 'o/update_youtube_dl.py'
etc['bin_update_freplace'] = 'o/tool/update_freplace.py'

# def Error
class UpdateError(Exception):
    pass

class NewVersionTooLowError(UpdateError):
    pass

# function

# load config file
def load_conf():
    # make root_path
    now_dir = os.path.dirname(__file__)
    root_path = os.path.join(now_dir, etc['to_root_path'])
    etc['root_path'] = root_path
    
    # make conf file path
    conf_path = os.path.join(root_path, etc['update_conf'])
    
    # read file
    with open(conf_path) as f:
        raw_text = f.read()
    # parse as json
    conf = json.loads(raw_text)
    etc['raw_conf'] = conf
    
    # read config item and set etc
    plugin_zip_file = conf['local']['plugin_zip_file']
    plugin_zip_file = os.path.join(root_path, plugin_zip_file)
    etc['plugin_zip_file'] = plugin_zip_file
    
    # process update_version path
    local_update_version = conf['local']['update_version']
    local_update_version = os.path.join(root_path, local_update_version)
    etc['local_update_version'] = local_update_version
    
    etc['remote_update_version'] = conf['remote']['update_version']
    
    # add py_bin
    etc['py_bin'] = sys.executable
    
    # process conf done

# parse update_version str
def parse_update_version(ver):
    # remove possible part after core update_version str
    t = ver.split('\r', 1)[0].split('\n', 1)[0]
    t = t.split('+', 1)[0].split('-', 1)[0]
    # split ver in 4 parts
    p = t.split('.')
    try:	# check update_version format
        for i in range(4):
            p[i] = int(p[i])
    except Exception as e:
        raise UpdateError('parse_update_version: update_version format ERROR, \"' + ver + '\" ', ver, e)
    # done
    return p

# check update_version
def check_version(old_ver, new_ver):
    '''
    return flag_should_update, flag_support_auto_replace
    
    check update_version, NOTE for update_version
    
    format
    	a.b.c.d
    example
    	0.0.1.0
    
    Each part is a int number. 
    
    Meanings of each part
    
    + a
    	If different, REFUSES to update. 
    	
    	raise Exception()
    + b
    	If different, able to update, 
    	but NOT support auto-file-replace. 
    	
    	return True, False
    	
    	Else, can use auto-file-replace. 
    	
    	return True, True
    	
    	WARNING: auto-file-replace is not supported now ! 
    + c
    	If different, should be updated. 
    	
    	return True, True
    + d
    	If different, should be updated. 
    	
    	return True, True
    
    '''
    # parse update_version str
    old = parse_update_version(old_ver)
    new = parse_update_version(new_ver)
    
    # check each part
    if old[0] > new[0]:	# old_ver > new_ver, refuse update
        raise NewVersionTooLowError(old, new)
    elif old[0] < new[0]: # old_ver > new_ver, refuse update
        raise UpdateError('update.check_version: REFUSE to update')
    elif old[1] > new[1]:	# ver[0] must be same, refuse update
        raise NewVersionTooLowError(old, new)
    elif old[1] < new[1]:	# allow update, but not support auto-file-replace
        return True, False
    elif old[2] > new[2]:	# ver[1] must be same, refuse update
        raise NewVersionTooLowError(old, new)
    elif old[2] < new[2]:	# allow update, and support auto-file-replace
        return True, True
    elif old[3] > new[3]:	# ver[2] must be same, refuse update
        raise NewVersionTooLowError(old, new)
    elif old[3] < new[3]:	# allow update
        return True, True
    else:	# all ver should be same
        return False, False	# no need to update
    # done

# rel_path
def rel_path(to_path, start='.'):
    from_path = os.path.abspath(start)
    to_path = os.path.abspath(to_path)
    r_path = os.path.relpath(to_path, start)
    return r_path

# network check update version
def network_check_update_version():
    local_update_version = etc['local_update_version']
    remote_update_version = etc['remote_update_version']
    
    # check remote_update_version
    r_update_ver_str = base.http_get(remote_update_version)
    print('update.update_network: [ OK ] got remote update_version [' + r_update_ver_str + '] from \"' + remote_update_version + '\"')
    
    # read local update_version
    with open(local_update_version) as f:
        l_update_ver_str = f.read()
    print('update.update_network: [ OK ] got local update_version [' + l_update_ver_str + '] from \"' + rel_path(local_update_version) + '\"')
    
    # check and cmp update_version str
    try:
        flag_should_update, flag_support_auto_replace = check_version(l_update_ver_str, r_update_ver_str)
        if flag_should_update:
            return True
        else:
            return False
    except NewVersionTooLowError as e:
        raise Exception('update.update_network: ERROR: [REFUSE update] remote version is older than local version ! ', e)
    # check update_version from network, done

# update from network
def update_network():
    # load config file
    load_conf()
    
    # check update_version
    if network_check_update_version():
        # update plugin and return local plugin zip bag file path
        exit_code = update_plugin()
        # check update result
        if exit_code != 0:
            raise Exception('update.update_network: ERROR: update plugin failed. ')
        # else:	# update OK
        # make local_zip file path
        local_zip = etc['plugin_zip_file']
        return local_zip
    else:	# only update sub
        exit_code = update_sub()
        # check update result
        if exit_code != 0:
            raise Exception('update.update_network: ERROR: update sub failed. ')
        # update OK
        return ''
    # done

# call sub update tools
def update_plugin():
    root_path = etc['root_path']
    py_bin = etc['py_bin']
    bin_update_plugin = etc['bin_update_plugin']
    bin_up = os.path.join(root_path, bin_update_plugin)
    
    arg = [py_bin, bin_up]
    print('\nupdate: ---> update-plugin :: run ' + str(arg) + ' \n')
    
    exit_code = run_sub.easy_run(arg)
    print('update: ---> update-plugin :: exit_code ' + str(exit_code) + ' ')
    return exit_code

def update_sub():
    root_path = etc['root_path']
    py_bin = etc['py_bin']
    bin_update_sub = etc['bin_update_sub']
    bin_us = os.path.join(root_path, bin_update_sub)
    
    arg = [py_bin, bin_us, '--no-pack']
    print('\nupdate: ---> update-sub :: run ' + str(arg) + ' \n')
    
    exit_code = run_sub.easy_run(arg)
    print('update: ---> update-sub :: exit_code ' + str(exit_code) + ' ')
    return exit_code

# update from local
def update_local(local_path):
    # NOTE not support local update now
    raise Exception('ERROR: not support local_update now (local path \"' + local_path + '\" ')

# end update.py



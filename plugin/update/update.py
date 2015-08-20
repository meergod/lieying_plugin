# -*- coding: utf-8 -*-
# update.py for lieying_plugin/module-update (plugin)
# plugin/update/update: plugin update function. 
# version 0.0.6.0 test201508071704

# import

import os
import sys
import json

from ..tool import base

# global vars
etc = {}	# global config info obj

etc['root_path'] = ''
etc['update_conf'] = ''	# update config file
etc['bin_update_plugin'] = 'update_plugin.py'
etc['bin_update_sub'] = 'update_sub.py'
etc['bin_update_freplace'] = 'file_replace.py'

# def Error
class UpdateError(Exception):
    pass

class NewVersionTooLowError(UpdateError):
    pass

# function

# load config file
def load_conf(flag_skip_read_conf_file=False):
    # check and get root_path
    if etc['root_path'] == '':
        root_path = base.make_root_path()
        etc['root_path'] = root_path
    
    # check skip_read_conf_file
    if flag_skip_read_conf_file:
        conf = etc['raw_conf']
    else:
        # check conf_file
        if etc['update_conf'] == '-':
            # NOTE should read from stdin
            conf_text = input()
            # NOTE now just read one line json text
        else:	# read from local conf_file
            # make conf file path
            conf_path = os.path.join(root_path, etc['update_conf'])
            
            # read file
            with open(conf_path) as f:
                conf_text = f.read()
        # parse as json
        conf = json.loads(conf_text)
        etc['raw_conf'] = conf
    
    # read config item and process it
    raw_tmp_path = conf['local']['tmp_path']
    tmp_path = os.path.join(root_path, raw_tmp_path)
    etc['tmp_path'] = tmp_path
    
    raw_plugin_zip_file = conf['local']['plugin_zip_file']
    plugin_zip_file = os.path.join(root_path, raw_plugin_zip_file)
    etc['plugin_zip_file'] = plugin_zip_file
    
    raw_local_update_version = conf['local']['update_version']
    local_update_version = os.path.join(root_path, raw_local_update_version)
    etc['local_update_version'] = local_update_version
    
    # add other useful items
    etc['remote_update_version'] = conf['remote']['update_version']
    etc['sub_list'] = conf['sub']
    etc['remote_plugin_zip'] = conf['remote']['plugin_zip']
    
    # add py_bin
    etc['py_bin'] = sys.executable
    
    # print info
    conf_file_str = etc['update_conf']
    if conf_file_str != '-':
        conf_file_str = '\"' + base.rel_path(conf_path) + '\"'
    print('update :: [ OK ] load config file ' + conf_file_str + '')
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

# network check update version
def network_check_update_version():
    local_update_version = etc['local_update_version']
    remote_update_version = etc['remote_update_version']
    
    # check remote_update_version
    r_update_ver_str = base.easy_dl(remote_update_version)
    ver_str = r_update_ver_str.split('\r', 1)[0].split('\n', 1)[0]
    print('update_network :: [ OK ] got remote update_version [' + ver_str + '] from \"' + remote_update_version + '\"')
    
    # read local update_version
    with open(local_update_version) as f:
        l_update_ver_str = f.read()
    ver_str = l_update_ver_str.split('\r', 1)[0].split('\n', 1)[0]
    print('update_network :: [ OK ] got local update_version [' + ver_str + '] from \"' + base.rel_path(local_update_version) + '\"')
    
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
    
    # print info
    print('update_network :: INFO: start update from network ')
    
    # load config file
    load_conf()
    
    # check update_version
    if network_check_update_version():
        # check sub
        sub_list = etc['sub_list']
        if len(sub_list) < 1:	# no sub
            # no need to re-pack, just return URL
            plugin_zip = etc['remote_plugin_zip']
            # DEBUG
            print('update_network :: INFO: just update from \"' + plugin_zip + '\" ')
            # done
            return plugin_zip
        
        # update plugin and return local plugin zip bag file path
        exit_code = update_plugin()
        # check update result
        if exit_code != 0:
            raise Exception('update.update_network: ERROR: update plugin failed. ')
        else:	# update OK
            print('update_network :: [ OK ] update plugin done. \n')
        # make local_zip file path
        local_zip = etc['plugin_zip_file']
        return local_zip
    else:	# only update sub
        # check sub
        sub_list = etc['sub_list']
        if len(sub_list) < 1:	# no need to update sub
            # DEBUG
            print('update_network :: INFO: no need to update. ')
            # done
            return ''
        # start update sub
        exit_code = update_sub()
        # check update result
        if exit_code != 0:
            raise Exception('update.update_network: ERROR: update sub failed. ')
        else:	# update OK
            print('update_network :: [ OK ] update sub done. ')
        return ''
    # done

# call sub update tools
def update_plugin():
    root_path = etc['root_path']
    py_bin = etc['py_bin']
    bin_update_plugin = etc['bin_update_plugin']
    bin_up = os.path.join(root_path, bin_update_plugin)
    
    arg = [py_bin, bin_up, '--config-file', '-']
    print('\nupdate_network :: ---> update-plugin :: run ' + str(arg) + ' \n')
    
    # make config text
    conf_text = json.dumps(etc['raw_conf']) + '\n\n'
    exit_code = base.run_write(arg, data=conf_text.encode('utf-8'))
    
    print('update_network :: ---> update-plugin :: exit_code ' + str(exit_code) + ' ')
    return exit_code

def update_sub():
    root_path = etc['root_path']
    py_bin = etc['py_bin']
    bin_update_sub = etc['bin_update_sub']
    bin_us = os.path.join(root_path, bin_update_sub)
    
    arg = [py_bin, bin_us, '--no-pack', '--config-file', '-']
    print('\nupdate_network :: ---> update-sub :: run ' + str(arg) + ' \n')
    
    # make config text
    conf_text = json.dumps(etc['raw_conf']) + '\n\n'
    exit_code = base.run_write(arg, data=conf_text.encode('utf-8'))
    
    print('update_network :: ---> update-sub :: exit_code ' + str(exit_code) + ' ')
    return exit_code

# update from local
def update_local(local_path):
    # NOTE not support local update now
    raise Exception('ERROR: not support local_update now (local path \"' + local_path + '\" ')

# end update.py



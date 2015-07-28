# -*- coding: utf-8 -*-
# update.py for lieying_plugin/youtube-dl (parse)
# plugin/update: plugin update function. 
# version 0.0.1.0 test201507281257

# import

import os

from . import run_sub

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

# end update.py



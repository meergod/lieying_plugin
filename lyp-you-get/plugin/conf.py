# -*- coding: utf-8 -*-
# conf.py for lieying_plugin/you-get (parse)
# plugin/conf: plugin config file support. 
# version 0.0.5.0 test201507270702

# import
import json
import sys
import os

# global vars

CONFIG_FILE = 'etc/lieying_plugin_config.json'
GET_ENCODING_TOOL = 'o/tool/get_encoding.py'

etc = {}	# config info

etc['you_get_bin'] = ''
etc['http_proxy'] = ''

etc['root_path'] = ''		# plugin root path
etc['py_bin'] = ''		# python bin file
etc['get_encoding_bin'] = ''	# get_encoding tool bin file

etc['encoding'] = {}
etc['encoding']['stdout'] = ''	# sys.stdout encoding
etc['encoding']['stderr'] = ''	# sys.stderr encoding

etc['flag_got_encoding'] = False

etc['flag_loaded'] = False

# function

# load config file
def load():
    
    # check loaded
    if etc['flag_loaded']:
        return True	# not load it again
    
    # add plugin root_path
    now_path = os.path.dirname(__file__)
    root_path = os.path.join(now_path, '../')	# plugin root path
    etc['root_path'] = root_path
    
    conf_file = os.path.join(root_path, CONFIG_FILE)
    info = load_json_file(conf_file)
    
    # read and set etc
    try:	# config file content error
        etc['you_get_bin'] = info['you_get_bin']
        etc['http_proxy'] = info['http_proxy']
    except Exception as e:
        raise Exception('plugin.conf: ERROR: config file content error', e)
    
    
    # process you_get_bin
    bin_path = os.path.join(root_path, etc['you_get_bin'])	# you_get_bin path is relative with plugin root path
    # update bin_path
    etc['you_get_bin'] = bin_path
    
    # add py_bin
    etc['py_bin'] = sys.executable
    # add get_encoding tool bin
    etc['get_encoding_bin'] = os.path.join(root_path, GET_ENCODING_TOOL)
    
    # done
    etc['flag_loaded'] = True
    return False

# base functions

def load_json_file(fpath):
    
    try:	# load config file error
        with open(fpath) as f:
            text = f.read()
    except Exception as e:
        raise Exception('plugin.conf: ERROR: read config file \"' + fpath + '\" failed', e)
    
    try:	# parse as json text error
        info = json.loads(text)
    except Exception as e:
        raise Exception('plugin.conf: ERROR: parse json text failed', e)
    
    return info

# end conf.py



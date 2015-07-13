# -*- coding: utf-8 -*-
# conf.py for lieying_plugin/flvgo (parse)
# plugin/conf: plugin config file support. 
# version 0.0.3.0 test201507131951

# import
import json
import os

# global vars

CONFIG_FILE = '../etc/lieying_plugin_config.json'

etc = {}	# config info

etc['flvgo_url'] = ''

etc['flag_loaded'] = False

# function

# load config file
def load():
    
    # check loaded
    if etc['flag_loaded']:
        return True	# not load it again
    
    conf_file = make_conf_file_path(CONFIG_FILE)
    info = load_json_file(conf_file)
    
    # read and set etc
    try:	# config file content error
        etc['flvgo_url'] = info['flvgo_url']
    except Exception as e:
        raise Exception('plugin.conf: ERROR: config file content error', e)
    
    # done
    etc['flag_loaded'] = True
    return False

# base functions

def make_conf_file_path(raw_path):
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, raw_path)
    return file_path

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



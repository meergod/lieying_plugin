# -*- coding: utf-8 -*-
# get_nosalt.py for lyp_bridge, lib/nosalt/get_nosalt, sceext <sceext@foxmail.com> 
# version 0.1.0.0 test201508190326

# import 

import os, json
import subprocess

from .. import conf

# global vars

etc = {}
etc['flag_gen_ed_path'] = False

# config items
etc['raw_slimerjs_bin'] = conf.slimerjs_bin	# path from plugin root path

etc['raw_open_page_bin'] = 'open_page.js'	# path from now_dir
etc['raw_root_path'] = '../../'	# from now_dir to plugin root path
# should be generated
etc['slimerjs_bin'] = ''
etc['open_page_bin'] = ''

# functions

# export functions

# get info from nosalt slimerjs open_page.js
def get_info(url):
    # gen paths
    gen_paths()
    # call sub and get info
    info = run_sub(url)
    # done
    return info

# base functions

# gen needed paths
def gen_paths():
    if etc['flag_gen_ed_path']:
        return True	# not re-gen
    # get now_dir
    now_dir = os.path.normpath(os.path.dirname(__file__))
    root_path = os.path.normpath(os.path.join(now_dir, etc['raw_root_path']))
    # gen open_page_bin
    open_page_bin = os.path.normpath(os.path.join(now_dir, etc['raw_open_page_bin']))
    etc['open_page_bin'] = open_page_bin	# save it
    # gen slimerjs bin path
    s_bin = os.path.normpath(os.path.join(root_path, etc['raw_slimerjs_bin']))
    etc['slimerjs_bin'] = s_bin
    # done
    return False

# try to decode, json should be {} format
def try_decode_json(raw):
    rest = raw
    while True:
        try:
            info = json.loads(rest)
            return info
        except Exception as e:
            # check string length
            if len(rest) < 2:
                raise Exception('get_nosalt :: try_decode_json failed. \n' + raw + '')
            # try to remove something before and after rest string
            if rest.startswith('{'):
                rest = rest[1:]
            rest = '{' + rest.split('{', 1)[1]
            if rest.endswith('}'):
                rest = rest[:-1]
            rest = rest.rsplit('}', 1)[0] + '}'
    # process done

# run sub
def run_sub(url):
    s_bin = etc['slimerjs_bin']
    op_bin = etc['open_page_bin']
    
    # check slimerjs_bin
    if not os.path.isfile(s_bin):
        raise Exception('get_nosalt :: ERROR: slimerjs not installed. File not exist \"' + s_bin + '\" ')
    
    # make args
    arg = [s_bin, op_bin, url]
    # start sub process
    PIPE = subprocess.PIPE
    p = subprocess.Popen(arg, stdout=PIPE, stderr=PIPE, shell=False)
    # get output
    stdout, stderr = p.communicate()
    # try to decdoe and load as json
    try:
        # FIXME may be decode BUG here
        # decode, just as utf-8
        stdout = stdout.decode('utf-8')
        info = try_decode_json(stdout)
        return info	# done
    except Exception as e:
        stderr = stderr.decode('utf-8', 'ignore')
        raise Exception('get_nosalt :: ERROR: get info from slimerjs sub failed. \n' + stdout + '\n' + stderr + ' ', e)
    # process done

# end get_nosalt.py



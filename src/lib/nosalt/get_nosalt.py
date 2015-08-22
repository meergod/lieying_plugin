# -*- coding: utf-8 -*-
# get_nosalt.py for lyp_bridge, lib/nosalt/get_nosalt, sceext <sceext@foxmail.com> 
# version 0.1.2.0 test201508220845

# import 

import re, os, sys
import subprocess

from .. import conf

# global vars

etc = {}
etc['flag_gen_ed_path'] = False

# config items
etc['raw_enhp_bin'] = 'enhp.js'	# path from now_dir
etc['raw_root_path'] = '../../'	# from now_dir to plugin root path
etc['node_bin'] = 'node'
# should be generated
etc['wb_proxy_bin'] = ''
etc['enhp_bin'] = ''

# TODO fix encoding BUG here
etc['stdout_encoding'] = 'utf-8'

# functions

# export functions

# get info from nosalt slimerjs open_page.js
def get_info(url):
    # gen paths
    gen_paths()
    # call sub and get info
    url = get_target(url)
    # done
    info = {}
    info['url'] = url
    return info

# base functions

# gen needed paths
def gen_paths():
    if etc['flag_gen_ed_path']:
        return True	# not re-gen
    # get now_dir
    now_dir = os.path.normpath(os.path.dirname(__file__))
    root_path = os.path.normpath(os.path.join(now_dir, etc['raw_root_path']))
    # gen enhp_bin
    enhp_bin = os.path.normpath(os.path.join(now_dir, etc['raw_enhp_bin']))
    etc['enhp_bin'] = enhp_bin	# save it
    # gen wb_proxy bin path
    w_bin = os.path.normpath(os.path.join(root_path, conf.wb_proxy_bin))
    etc['wb_proxy_bin'] = w_bin
    # done
    return False

# parse enhp output
def parse_enhp(raw):
    part = raw.split(' ', 2)
    url = part[2]
    return url

# get target, main work function
def get_target(url):
    w_bin = etc['wb_proxy_bin']
    p_bin = etc['enhp_bin']
    node_bin = etc['node_bin']
    
    p_port = conf.local_proxy_port
    
    PIPE = subprocess.PIPE
    # start enhp
    p_arg = [node_bin, '--harmony', p_bin, str(p_port)]
    # print for DEBUG
    print('DEBUG: start enhp proxy server at port ' + str(p_port) + ' ')
    pp = subprocess.Popen(p_arg, stdout=PIPE, stderr=sys.stderr, shell=False)
    # wait until enhp init finished
    pp.stdout.readline()
    
    # make args for wb_proxy
    local_proxy = '127.0.0.1:' + str(p_port)
    # start wb_proxy.exe
    w_arg = [w_bin, local_proxy, url]
    pw = subprocess.Popen(w_arg, stdout=None, stderr=sys.stderr, shell=False)
    
    # get and check enhp output
    encoding = etc['stdout_encoding']
    re_target = conf.re_target_url
    while True:
        raw = pp.stdout.readline()
        one = raw.decode(encoding)
        # remove \r \n after end
        if one.endswith('\r\n'):
            one = one[:-len('\r\n')]
        elif one.endswith('\r') or one.endswith('\n'):
            one = one[:-1]
        # decode it
        url = parse_enhp(one)
        # check url
        if len(re.findall(re_target, url)) > 0:
            # kill both process
            pw.kill()
            pp.kill()
            # just return the result
            return url
    # check done, and get target URL, done OK

# end get_nosalt.py



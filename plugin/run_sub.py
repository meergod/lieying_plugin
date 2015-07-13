# -*- coding: utf-8 -*-
# run_sub.py for lieying_plugin/you-get (parse)
# plugin/run_sub: run subprocess
# version 0.0.3.0 test201507131417

# import

import os
import sys
import subprocess

from . import conf

# function

def run(args, shell=False):
    
    PIPE = subprocess.PIPE
    
    p = subprocess.Popen(args, stdout=PIPE, stderr=PIPE, shell=shell)
    
    stdout, stderr = p.communicate()
    
    return stdout, stderr

def check_file(fpath):
    if os.path.isfile(fpath):
        return True
    return False

# run you_get function
def run_you_get(args):
    
    # load config
    conf.load()
    # get you_get_bin
    you_get_bin = conf.etc['you_get_bin']
    # check file
    if not check_file(you_get_bin):
        raise Exception('plugin.run_sub: ERROR: you-get bin file not exist \"' + you_get_bin + '\" ')
    
    # get python bin
    py_bin = sys.executable
    
    arg = []
    # check and add http_proxy
    if conf.etc['http_proxy'] != '':
        arg += ['--extractor-proxy', conf.etc['http_proxy']]
    
    # make final args
    arg = [py_bin, you_get_bin] + arg + args
    
    # just run you_get
    stdout, stderr = run(arg)
    # decode as text, NOTE encoding may be a problem
    stdout = stdout.decode()
    stderr = stderr.decode()
    # done
    return stdout, stderr

# end run_sub.py



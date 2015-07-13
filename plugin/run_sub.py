# -*- coding: utf-8 -*-
# run_sub.py for lieying_plugin/you-get (parse)
# plugin/run_sub: run subprocess
# version 0.0.1.0 test201507131406

# import

import os
import subprocess

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

# end run_sub.py



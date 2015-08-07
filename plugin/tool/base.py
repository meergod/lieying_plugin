# -*- coding: utf-8 -*-
# base.py for lieying_plugin [sceext] plugin/tool, common tools
# plugin/tool/base: base functions
# version 0.0.4.0 test201508071515

# import

import os
import sys
import math
import subprocess

# global vars

ROOT_PATH = '../../'

# functions


# ## text functions

# convert size_byte number to human readable text
def byte2size(size_byte, flag_add_bytes=False):
    
    unit_list = [
        'Byte', 
        'KB', 
        'MB', 
        'GB', 
        'TB', 
        'PB', 
        'EB', 
    ]
    
    # check use Byte
    if size_byte < 1024:
        size = str(size_byte) + ' Byte'
        return size
    
    # get unit
    unit_i = math.floor(math.log(size_byte, 1024))
    unit = unit_list[unit_i]
    size_n = size_byte / pow(1024, unit_i)
    
    size_t = float_len(size_n, 2)
    
    # make final size_str
    size_str = size_t + ' ' + unit
    
    # check and add Byte
    if flag_add_bytes:
        size_str += ' (' + str(size_byte) + ' Byte)'
    # done
    return size_str

# make a float number to a fixed
def float_len(n, l=2):
    
    f = float(n)
    t = str(f).split('.', 1)
    
    # delete chars
    while len(t[1]) > l:
        t[1] = t[1][:-1]
    
    # add zeros
    while len(t[1]) < l:
        t[1] += '0'
    
    # done
    nt = ('.').join(t)
    return nt

# add zero before number str
def zero_len(n, l=2):
    t = str(int(n))
    while len(t) < l:
        t = '0' + t
    return t


# ## path functions

# get rel_path from now by default
def rel_path(base_path, start='.'):
    now_path = os.path.abspath(start)
    b_path = os.path.abspath(base_path)
    r_path = os.path.normpath(os.path.relpath(b_path, start=now_path))
    return r_path

# check a file is a normal file
def check_file(fpath):
    if os.path.isfile(fpath):
        return True
    return False

# get plugin root_path
def make_root_path():
    now_path = os.path.dirname(__file__)
    raw_root_path = os.path.join(now_path, ROOT_PATH)
    root_path = os.path.normpath(raw_root_path)
    return root_path

# make file list of a given path, file list to add to the zip file
def gen_file_list(base_path):
    
    # get raw_list
    raw_list, dir_list = gen_file_list_base(base_path)
    # count something
    
    count_size = 0
    for f in raw_list:
        count_size += f['size']
        # remove base_path in file name
        f['name'] = os.path.relpath(f['name'], base_path)
    # make output info
    out = {}
    out['list'] = raw_list
    out['count'] = len(raw_list)
    out['size'] = count_size
    # remove dir_list base_path like raw_list
    for d in dir_list:
        d['name'] = os.path.relpath(d['name'], base_path)
    out['dir_list'] = dir_list
    out['dir_count'] = len(dir_list)
    # done
    return out

def gen_file_list_base(base_path):
    out = []
    dir_list = []
    if not os.path.isdir(base_path):
        return out, dir_list
    # list sub
    sub_list = os.listdir(base_path)
    for s in sub_list:
        fpath = os.path.join(base_path, s)
        if os.path.islink(fpath):
            continue	# ignore link files
        elif os.path.isfile(fpath):
            # get file info and add this
            fsize = os.path.getsize(fpath)
            
            one = {}
            one['name'] = fpath
            one['size'] = fsize
            
            out.append(one)
        elif os.path.isdir(fpath):
            # add it to dir_list
            one = {}
            one['name'] = fpath
            
            dir_list.append(one)
            
            # re-call gen_file_list_base to get sub info
            sub_info, sub_dir = gen_file_list_base(fpath)
            out += sub_info
            dir_list += sub_dir
    # process get list all sub info done
    return out, dir_list

# file function

# mv -R, move dir
def mv_R(old, new):
    os.renames(old, new)

# find first dir
def find_first_dir(base_path):
    
    sub_list = os.listdir(base_path)
    for s in sub_list:
        fpath = os.path.join(base_path, s)
        if os.path.isdir(fpath):
            return fpath
    return None

# remove dirs, rm -r
def rm_R(base_path):
    
    # get file list
    finfo = gen_file_list(base_path)
    
    # remove each file
    dir_ok_count = 0
    dir_err_count = 0
    file_ok_count = 0
    file_err_count = 0
    byte_ok_count = 0
    byte_err_count = 0
    
    # remove all files
    for f in finfo['list']:
        try:
            fpath = os.path.join(base_path, f['name'])
            os.remove(fpath)
            
            # add count
            file_ok_count += 1
            byte_ok_count += f['size']
        except OSError:	# delete file failed
            # add count
            file_err_count += 1
            byte_err_count += f['size']
    # remove all dirs
    # NOTE from last to first to delete
    dir_count = len(finfo['dir_list'])
    i = dir_count - 1
    while i >= 0:
        d = finfo['dir_list'][i]
        i -= 1
        try:
            fpath = os.path.join(base_path, d['name'])
            os.rmdir(fpath)
            
            # add count
            dir_ok_count += 1
        except OSError:	# remove failed
            dir_err_count += 1
    # output count
    count = {}
    count['ok'] = {}
    count['err'] = {}
    count['ok']['file'] = file_ok_count
    count['ok']['dir'] = dir_ok_count
    count['ok']['byte'] = byte_ok_count
    count['err']['file'] = file_err_count
    count['err']['dir'] = dir_err_count
    count['err']['byte'] = byte_err_count
    return count
    # done


# ## subprocess functions

# run subprocess, just get exit_code
def easy_run(arg, shell=False):
    p = subprocess.Popen(arg, shell=shell)
    exit_code = p.wait()
    return exit_code

# run subprocess, and get stderr, stdout
def run(args, shell=False):
    PIPE = subprocess.PIPE
    p = subprocess.Popen(args, stdout=PIPE, stderr=PIPE, shell=shell)
    stdout, stderr = p.communicate()
    return stdout, stderr

# run subprocess, and write its stdin
def run_write(args, shell=False, data=b''):
    PIPE = subprocess.PIPE
    p = subprocess.Popen(args, stdin=PIPE, shell=shell)
    # write data
    p.stdin.write(data)
    # done, just get exit_code
    exit_code = p.wait()
    return exit_code

# ## network functions

# simple download method, just return the content as text
def easy_dl(url):
    r = urllib.request.urlopen(url)
    raw = r.read()
    text = raw.decode('utf-8', 'ignore')
    return text


# end base.py



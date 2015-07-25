# -*- coding: utf-8 -*-
# main.py for lieying_plugin
# o/update/main: plugin update function, main file
# version 0.0.2.0 test201507251027

# import

import json

from . import make_zip
from . import github

# global vars
etc = {}	# global config info

etc['conf'] = {}	# loaded from config file
etc['conf_loaded'] = False	# prevent reload flag
etc['root_path'] = ''	# plugin root path

PLUGIN_ROOT_PATH = '../../'
PLUGIN_UPDATE_PATH = 'o/update'

# function

# text function
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
    
    size_t = float_len(size_n)
    
    # make final size_str
    size_str = size_t + ' ' + unit
    
    # check and add Byte
    if flag_add_bytes:
        size_str += ' (' + str(size_byte) + ' Byte)'
    # done
    return size_str

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


# read given config file (json) and put info in etc
def load_config(fpath, force_reload=False):
    # check loaded flag
    if etc['conf_loaded'] and (not force_reload):
        return True	# not reload by default
    
    # read file
    with open(fpath) as f:
        raw_text = f.read()
    
    # parse json
    info = json.loads(raw_text)
    # load config file done
    etc['conf'] = info
    
    # add plugin root path
    now_path = os.dirname(__file__)
    root_path = os.path.join(now_path, PLUGIN_ROOT_PATH)
    etc['root_path'] = root_path
    
    # update loaded flag
    etc['conf_loaded'] = True
    # done
    return False


# network function

# check github latest commit
def check_github_latest_commit(github_page_url):
    # download page html_text
    html_text = github.easy_dl(github_page_url)
    # get latest commit str
    latest_commit = github.get_latest_commit(html_text)
    # done
    return latest_commit

# dl file
def dl_file(url, fpath):
    return github.file_dl(url, fpath)


# file function

# mv -R, move dir
def mv_R(old, new):
    os.renames(old_new)

# find first dir
def find_first_dir(base_path):
    
    sub_list = os.listdir(base_path)
    for s in sub_list:
        if os.isdir(s):
            fpath = os.path.join(base_path, s)
            return fpath
    return None

# remove dirs, rm -r
def rm_R(base_path):
    
    # get file list
    finfo = make_zip.gen_file_list(base_path)
    
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
    for d in finfo['dir_list']:
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

# end main.py



# -*- coding: utf-8 -*-
# main.py for lieying_plugin/module-update (plugin)
# plugin/update/main: plugin update function, main file
# version 0.0.12.0 test201508071529

# import

import os
import json

from . import github
from . import make_zip
from . import update

from ..tool import base

# global vars
etc = update.etc	# NOTE this is the same as update.etc

etc['conf_loaded'] = False	# prevent reload flag

# function

# just use update.load_conf
def load_config(force_reload=False):
    # check loaded flag
    if etc['conf_loaded'] and (not force_reload):
        return True	# not reload by default
    
    # do load it
    update.load_conf()
    
    # update loaded flag
    etc['conf_loaded'] = True
    # done
    return False

# network function

# check github latest commit
def check_github_latest_commit(github_page_url):
    # download page html_text
    html_text = base.easy_dl(github_page_url)
    # get latest commit str
    latest_commit = github.get_latest_commit(html_text)
    
    # get archive zip url from github page html
    zip_url = github.get_zip_url(html_text, github_page_url)
    
    # done
    return latest_commit, zip_url

# dl file
def dl_file(url, fpath):
    return github.file_dl(url, fpath)

# clean dir path
def clean_dir(base_path):
    cinfo = base.rm_R(base_path)	# count info
    cleaned_count = cinfo['ok']['file'] + cinfo['err']['file']
    real_count = cleaned_count + cinfo['ok']['dir'] + cinfo['err']['dir']
    if real_count > 0:
        t = 'update: [ OK ] clean ' + str(cleaned_count) + ' exists files from \"' + base.rel_path(base_path) + '\" \n'
        t += '      OK ' + str(cinfo['ok']['file']) + ' files, '
        t += str(cinfo['ok']['dir']) + ' dirs, '
        t += base.byte2size(cinfo['ok']['byte']) + ' \n'
        t += '  FAILED ' + str(cinfo['err']['file']) + ' files, '
        t += str(cinfo['err']['dir']) + ' dirs, '
        t += base.byte2size(cinfo['err']['byte']) + ' '
        print(t)
    else:
        print('update: INFO: no need to clean \"' + base.rel_path(base_path) + '\"')
    # done
    return real_count


# extract zip file to a path
def extract_pack(zip_file, extract_path, msg=''):
    
    print('update: INFO: extract ' + msg + ' to \"' + base.rel_path(extract_path) + '\" ')
    # get file list
    finfo = make_zip.get_file_list(zip_file)
    t = 'update: [ OK ] got file list, '
    t += str(finfo['count']) + ' files, '
    t += base.byte2size(finfo['size'], True)
    t += ' (' + base.byte2size(finfo['zsize']) + ') '
    print(t)
    
    # delete exist files
    if clean_dir(extract_path) > 0:
        clean_dir(extract_path)	# NOTE clean 2 times
    
    # do extract zip file
    make_zip.extract_zip_file(zip_file, finfo['list'], extract_path)
    print('update: [ OK ] extract zip file done')
    # done

# moving files
def mv_file(path_from, path_to):
    
    # before move, delete exist files
    if clean_dir(path_to) > 0:
        clean_dir(path_to)	# NOTE clean 2 times
    
    # NOTE before move files, delete to dir, FIX BUG on windows
    try:
        os.rmdir(path_to)
    except OSError:
        print('update: WARNING: delete dir failed \"' + path_to + '\" ')
    
    # move files
    print('update: INFO: move files from \"' + base.rel_path(path_from) + '\" to \"' + base.rel_path(path_to) + '\" ')
    base.mv_R(path_from, path_to)
    # done


# end main.py



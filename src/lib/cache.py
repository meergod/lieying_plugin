# -*- coding: utf-8 -*-
# cache.py for lyp_bridge, lib/cache, sceext <sceext@foxmail.com> 
# version 0.0.2.0 test201508190043

# import
import os

# global vars
CACHE_DIR = '../cache'	# from now_dir
CACHE_ITEM_AFTER = 'jsonaddr'	# NOTE cache file sample 'v_19rro7ou14jsonaddr'

etc = {}
etc['cache_path'] = ''	# cache dir full path

# functions

# export function

# update one cache item, write url's info
def update(url, info):
    make_cache_dir()
    fname = make_file_name(url)
    # make cache file full name
    full = os.path.normpath(os.path.join(etc['cache_path'], fname))
    # write file
    with open(full, 'w') as f:
        f.write(info)
    # done
    return fname

# base functions

# gen cache file name, by given url
def make_file_name(url):
    # remove http://
    t = url.split('://', 1)[1]
    # remove ?
    t = t.split('?', 1)[0]
    # remove site name until /
    t = t.split('/', 1)[1]
    # remove .html
    t = t.rsplit('.', 1)[0]
    # now t is the raw name
    name = t + CACHE_ITEM_AFTER
    # done
    return name

# generate cache dir
def make_cache_dir():
    # check if path is null
    if etc['cache_path'] != '':
        return True	# not re-make
    # get now dir
    now_dir = os.path.normpath(os.path.dirname(__file__))
    cache_dir = os.path.normpath(os.path.join(now_dir, CACHE_DIR))
    # try to create dir
    if not os.path.isdir(cache_dir):
        os.mkdir(cache_dir)
    # save it
    etc['cache_path'] = cache_dir
    # done
    return False

# end cache.py



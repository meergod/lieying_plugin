#!/usr/bin/env python
# -*- coding: utf-8 -*-
# update_sub.py for lieying_plugin/module-update (plugin)
# update_sub: plugin update sub function, 
#     auto download sub s from github and 
#     auto re-pack plugin zip bag
# version 0.0.19.0 test201508071719

# NOTE supported command line args
#	--no-pack	not pack a AUTO-PACK zip file in tmp/
#	--pack-only	not check latest commit on github and 
#			not download zip file from github
#			just pack a AUTO-PACK zip file in tmp/
#	--force		force download zip file from github
#			even if latest commit is same
#	--config-file	load from this config file
#	--re-pack-file	define re-pack generated file
#	--root-path	set root_path

# import

import os
import sys
import datetime

from plugin.tool import base
from plugin.update import main
from plugin.update import make_zip

# global vars

PLUGIN_UPDATE_TOOL_VERSION = 'lieying_plugin update_tool version 0.0.6.0 test201508071719'

etc = {}	# global config info

# flags to support command line args
etc['flag_dl_github'] = True
etc['flag_pack_zip'] = True
etc['flag_force'] = False	# NOTE default value should be False
etc['re_pack_file'] = ''

# function

def main():
    
    # init info
    print('update_sub: INFO: start update ')
    
    # get and process command line args
    get_args()
    
    # use main load config file function
    main.load_config()
    conf = main.etc['raw_conf']
    etc['conf'] = conf
    etc['root_path'] = main.etc['root_path']
    tmp_path = main.etc['tmp_path']
    etc['tmp_path'] = tmp_path
    
    # check flags
    if etc['flag_dl_github']:
        # process sub
        process_sub()
        # update local latest commit, NOTE update local latest commit file before re-pack
        update_local_latest_commit()
    # check and download from github, done
    
    # check flag
    if etc['flag_pack_zip']:
        # check and generate re_pack_file
        if etc['re_pack_file'] == '':
            zip_file = conf['local']['re_pack_file'] + make_re_pack_name() + '.zip'
            zip_path = os.path.join(tmp_path, zip_file)
            etc['re_pack_file'] = zip_path
        # re-pack
        re_pack()
    
    # done
    print('update_sub: [ OK ] done. All works finished. ')

# process command line args
def get_args():
    args = sys.argv
    arg = args[1:]
    # process each arg
    rest = arg
    while len(rest) > 0:
        one = rest[0]
        rest = rest[1:]
        # check this arg
        if one == '--no-pack':
            # set global flag
            etc['flag_pack_zip'] = False
            # info
            print('update_sub: INFO: got [' + one + '], not pack zip file. ')
        elif one == '--pack-only':
            # set flag
            etc['flag_dl_github'] = False
            # info
            print('update_sub: INFO: got [' + one + '], not check and download from github. ')
        elif one == '--force':
            etc['flag_force'] = True
            
            print('update_sub: INFO: got [' + one + '], ignore latest commit check result. ')
        elif one == '--config-file':
            conf_file = rest[0]
            rest = rest[1:]
            # set it to main
            main.etc['update_conf'] = conf_file
        elif one == '--re-pack-file':
            pack_file = rest[0]
            rest = rest[1:]
            # set it
            etc['re_pack_file'] = pack_file
        elif one == '--root-path':
            root_path = rest[0]
            rest = rest[1:]
            # set it
            main.set_root_path(root_path)
        else:	# unknow option
            print('update_sub: WARNING: unknow option [' + one + '] ')
    # process args done

# process sub
def process_sub():
    # get sub list
    sub_list = etc['sub_list']
    # process each sub
    for one in sub_list:
        process_one_sub(one)
    # done

# process one sub
def process_one_sub(sub_item):
    sub_name = sub_item['sub_name']
    # check latest commit
    if not check_latest_commit(sub_item):
        # no need to update
        print('update_sub: [' + sub_name + '] done')
        return
    
    # start real update
    zip_url = sub_item['g_zip_url']
    print('update_sub: INFO: download ' + sub_name + ' zip file from \"' + zip_url + '\" ')
    
    tmp_path = etc['tmp_path']
    
    # pre process zip_url
    zip_url2 = zip_url.split('://')[1].split('?')[0]
    # make zip file path
    zip_file = os.path.join(tmp_path, os.path.basename(zip_url2))
    if not (zip_file.endswith('.zip')):
        zip_file += '.zip'
    # do download
    ed_byte = main.dl_file(zip_url, zip_file)
    # download info
    print('update_sub: [ OK ] saved ' + base.byte2size(ed_byte, True) + ' to \"' + base.rel_path(zip_file) + '\"')
    
    sub_item['zip_file'] = zip_file
    
    # extract zip file
    extract_pack(sub_item)
    # move files
    mv_file(sub_item)
    # done

# update local latest commit
def update_local_latest_commit():
    # get config
    root_path = etc['root_path']
    tmp_path = etc['tmp_path']
    
    # get sub list
    conf = etc['conf']
    sub_list = conf['sub']
    
    # process each item
    for one in sub_list:
        # check sub_type
        sub_type = one['sub_type']
        if sub_type != 'github':
            continue	# just ignore it
        sub_name = one['sub_name']
        local_commit_file = one['local_latest_commit']
        # add root_path
        local_file = os.path.join(root_path, local_commit_file)
        # remote latest commit str
        latest_commit = one['latest_commit']
        # just update it
        update_one_latest_commit(sub_name=sub_name, latest_commit=latest_commit, local_file=local_file)
    # done

# update one local latest commit
def update_one_latest_commit(sub_name='[unknow]', latest_commit='[ERROR]', local_file='[bad file]'):
    # update latest commit
    print('update_sub: INFO: save ' + sub_name + '\'s latest commit [' + latest_commit + '] to \"' + base.rel_path(local_file) + '\" ')
    with open(local_file, 'w') as f:
        f.write(latest_commit)
    # done


# check lastest commit
def check_latest_commit(sub_item):
    sub_name = sub_item['sub_name']
    sub_type = sub_item['sub_type']
    # check sub_type
    if sub_type != 'github':
        print('update_sub: WARNING: ignore check latest commit for [' + sub_name + '] of type [' + sub_type + '] ')
    print('update_sub: INFO: checking latest commit for [' + sub_name + '] ')
    
    # get github latest commit
    page_url = sub_item['sub_home']
    print('update_sub: INFO: load github page \"' + page_url + '\" ')
    g_latest_commit, g_zip_url = main.check_github_latest_commit(page_url)
    print('update_sub: [ OK ] got latest commit [' + g_latest_commit + ']')
    
    # save g_zip_url
    sub_item['g_zip_url'] = g_zip_url
    
    # save latest_commit
    sub_item['latest_commit'] = g_latest_commit
    
    # get local latest commit
    l_latest_commit = ''
    local_file = sub_item['local_latest_commit']
    root_path = etc['root_path']
    fpath = os.path.join(root_path, local_file)
    try:
        with open(fpath) as f:
            l_latest_commit = f.read().split('\n')[0].split('\r')[0]
    except OSError:
        print('update_sub: ERROR: can not open local commit info file \"' + base.rel_path(fpath) + '\" ')
        return True
    # got local latest commit
    print('update_sub: [ OK ] local commit [' + l_latest_commit + ']')
    
    # check match
    if l_latest_commit == g_latest_commit:
        # check force flag
        if etc['flag_force']:
            print('update_sub: INFO: ignore latest commit check result. ')
        else:
            print('update_sub: INFO: no need to update. ')
            return False
    else:	# should update
        print('update_sub: INFO: start real update')
    return True


# extract youtube-dl
def extract_pack(sub_item):
    
    zip_file = sub_item['zip_file']
    tmp_path = etc['tmp_path']
    
    # make extract path
    extract_path = os.path.join(tmp_path, sub_item['extract_path'])
    sub_item['extracted_path'] = extract_path
    
    # extract file
    main.extract_pack(zip_file, extract_path, msg=sub_item['sub_name'])

# moving files
def mv_file(sub_item):
    extract_path = sub_item['extracted_path']
    root_path = etc['root_path']
    
    # moving files
    sub_path = os.path.join(root_path, sub_item['sub_path'])
    # got extracted youtube-dl path
    extracted_path = base.find_first_dir(extract_path)
    
    # use command move function
    base.mv_file(extracted_path, sub_path)

# re-packing plugin zip bag
def re_pack(compress=make_zip.zipfile.ZIP_DEFLATED):
    
    root_path = etc['root_path']
    tmp_path = etc['tmp_path']
    conf = etc['conf']
    
    # start re-pack
    print('update_sub: INFO: start re-pack plugin zip bag file ')
    
    # get file list
    finfo = base.gen_file_list(root_path)
    
    tmp_path_short = os.path.relpath(tmp_path, root_path)
    # ignore some from flist
    flist = []	# keep file list
    ilist = []	# ignored file list
    for f in finfo['list']:
        # ignore .git
        if f['name'].startswith('.git'):
            ilist.append(f)
        # ignore __pycache__
        elif '__pycache__' in f['name']:
            ilist.append(f)
        # ignore tmp path
        elif f['name'].startswith(tmp_path_short):
            ilist.append(f)
        else:	# should keep this file
            flist.append(f)
    # count something
    isize = 0
    fsize = 0
    for f in ilist:
        isize += f['size']
    for f in flist:
        fsize += f['size']
    # print info
    t = 'update_sub: [ OK ] make file list done, ' + str(len(flist)) + ' files, '
    t += base.byte2size(fsize, True) + '; '
    t += 'ignored ' + str(len(ilist)) + ' files, ' + base.byte2size(isize) + '. '
    print(t)
    
    # create zip file
    zip_path = etc['re_pack_path']
    print('update_sub: INFO: create zip file \"' + base.rel_path(zip_path) + '\" ')
    
    make_zip.make_zip_file(zip_path, flist, root_path, compress=compress)
    
    # compress done
    print('update_sub: [ OK ] compress files done. ')

# make auto-pack zip file name
def make_re_pack_name():
    zero_len = base.zero_len
    now = datetime.datetime.now()
    t = zero_len(now.year, 4) + '-'
    t += zero_len(now.month, 2) + '-'
    t += zero_len(now.day, 2) + '_'
    t += zero_len(now.hour, 2) + '-'
    t += zero_len(now.minute, 2) + '-'
    t += zero_len(now.second, 2)
    return t


# start from main
if __name__ == '__main__':
    main()

# end update_sub.py



#!/usr/bin/env python
# -*- coding: utf-8 -*-
# update_youtube_dl.py for lieying_plugin
# o/update_youtube_dl: plugin update function, 
#     auto download youtube-dl from github and 
#     auto re-pack plugin zip bag
# version 0.0.3.0 test201507251239

# import

import os
import datetime

from update import main as update
from update import make_zip

# global vars
CONFIG_FILE = 'etc/update_config.json'

etc = {}	# global config info

# function

def main():
    
    # init info
    print('update: INFO: start update youtube-dl ')
    
    # load config file
    update.load_config(CONFIG_FILE)
    
    print('update: [ OK ] load config file \"' + os.path.relpath(CONFIG_FILE, '.') + '\"')
    
    # check latest commit
    if not check_latest_commit():
        # no need to update
        print('update: done')
        return
    
    conf = update.etc['conf']
    # start real update
    zip_url = conf['remote']['youtube_dl_zip']
    print('update: INFO: download youtube-dl zip file from \"' + zip_url + '\" ')
    
    root_path = update.etc['root_path']
    tmp_path = os.path.join(root_path, conf['local']['tmp_path'])
    etc['tmp_path'] = tmp_path
    
    # make zip file path
    zip_file = os.path.join(tmp_path, os.path.basename(zip_url))
    if not (zip_file.endswith('.zip')):
        zip_file += '.zip'
    # do download
    ed_byte = update.dl_file(zip_url, zip_file)
    # download info
    print('update: [ OK ] saved ' + update.byte2size(ed_byte, True) + ' to \"' + zip_file + '\"')
    
    etc['zip_file'] = zip_file
    
    # extract zip file
    extract_pack()
    # move files
    mv_file()
    
    # re-pack
    re_pack()
    
    latest_commit_file = conf['local']['youtube_dl_latest_commit']
    latest_commit_file = os.path.join(root_path, latest_commit_file)
    g_latest_commit = etc['g_latest_commit']
    # update latest commit
    print('update: INFO: save latest commit [' + g_latest_commit + '] to \"' + os.path.relpath(latest_commit_file, '.') + '\" ')
    with open(latest_commit_file, 'w') as f:
        f.write(g_latest_commit)
    # done
    print('update: [ OK ] done. All works finished. ')


# check lastest commit
def check_latest_commit():
    print('update: INFO: checking latest commit ')
    
    conf = update.etc['conf']
    # get github latest commit
    page_url = conf['remote']['youtube_dl_home']
    
    print('update: INFO: load github page \"' + page_url + '\" ')
    g_latest_commit = update.check_github_latest_commit(page_url)
    print('update: [ OK ] got latest commit [' + g_latest_commit + ']')
    
    # save latest_commit
    etc['g_latest_commit'] = g_latest_commit
    
    # get local latest commit
    l_latest_commit = ''
    local_file = conf['local']['youtube_dl_latest_commit']
    root_path = update.etc['root_path']
    fpath = os.path.join(root_path, local_file)
    try:
        with open(fpath) as f:
            l_latest_commit = f.read().split('\n')[0].split('\r')[0]
    except OSError:
        print('update: ERROR: can not open local commit info file \"' + os.path.relpath(fpath, '.') + '\" ')
        return True
    # got local latest commit
    print('update: [ OK ] local commit [' + l_latest_commit + ']')
    
    # check match
    if l_latest_commit == g_latest_commit:
        print('update: INFO: no need to update. ')
        return False
    # should update
    print('update: INFO: start real update')
    return True

# clean dir path
def clean_dir(base_path):
    cinfo = update.rm_R(base_path)	# count info
    cleaned_count = cinfo['ok']['file'] + cinfo['err']['file']
    real_count = cleaned_count + cinfo['ok']['dir'] + cinfo['err']['dir']
    if real_count > 0:
        t = 'update: [ OK ] clean ' + str(cleaned_count) + ' exists files from \"' + base_path + '\" \n'
        t += '      OK ' + str(cinfo['ok']['file']) + ' files, '
        t += str(cinfo['ok']['dir']) + ' dirs, '
        t += update.byte2size(cinfo['ok']['byte']) + ' \n'
        t += '  FAILED ' + str(cinfo['err']['file']) + ' files, '
        t += str(cinfo['err']['dir']) + ' dirs, '
        t += update.byte2size(cinfo['err']['byte']) + ' '
        print(t)
    # done

# extract youtube-dl
def extract_pack():
    
    zip_file = etc['zip_file']
    conf = update.etc['conf']
    tmp_path = etc['tmp_path']
    
    # extract file
    extract_path = os.path.join(tmp_path, conf['local']['youtube_dl_extract_path'])
    etc['extract_path'] = extract_path
    print('update: INFO: extract youtube-dl to \"' + extract_path + '\" ')
    # get file list
    finfo = make_zip.get_file_list(zip_file)
    t = 'update: [ OK ] got file list, '
    t += str(finfo['count']) + ' files, '
    t += update.byte2size(finfo['size'], True)
    t += ' (' + update.byte2size(finfo['zsize']) + ') '
    print(t)
    
    # delete exist files
    clean_dir(extract_path)
    clean_dir(extract_path)	# NOTE clean 2 times, fix BUGs here
    
    # do extract zip file
    make_zip.extract_zip_file(zip_file, finfo['list'], extract_path)
    print('update: [ OK ] extract zip file done')

# moving files
def mv_file():
    extract_path = etc['extract_path']
    root_path = update.etc['root_path']
    conf = update.etc['conf']
    
    # moving files
    youtube_dl_path = os.path.join(root_path, conf['local']['youtube_dl_path'])
    # got extracted youtube-dl path
    extracted_path = update.find_first_dir(extract_path)
    
    # before move, delete exist files
    clean_dir(youtube_dl_path)
    clean_dir(extract_path)	# NOTE clean 2 times, fix BUGs here
    # move files
    print('update: INFO: move files from \"' + os.path.relpath(extracted_path, '.') + '\" to \"' + os.path.relpath(youtube_dl_path, '.') + '\" ')
    update.mv_R(extracted_path, youtube_dl_path)
    # done

# re-packing plugin zip bag
def re_pack():
    
    root_path = update.etc['root_path']
    conf = update.etc['conf']
    tmp_path = etc['tmp_path']
    
    # start re-pack
    print('update: INFO: start re-pack plugin zip bag file ')
    
    # get file list
    finfo = make_zip.gen_file_list(root_path)
    
    # ignore some from flist
    flist = []	# keep file list
    ilist = []	# ignored file list
    for f in finfo['list']:
        # ignore .git
        if '.git' in f['name']:
            ilist.append(f)
        # ignore __pycache__
        elif '__pycache__' in f['name']:
            ilist.append(f)
        # ignore tmp path
        elif f['name'].startswith(tmp_path):
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
    t = 'update: [ OK ] make file list done, ' + str(len(flist)) + ' files, '
    t += update.byte2size(fsize, True) + '; '
    t += 'ignored ' + str(len(ilist)) + ' files, ' + update.byte2size(isize) + '. '
    print(t)
    
    # create zip file
    zip_file = conf['local']['re_pack_file'] + make_re_pack_name() + '.zip'
    zip_path = os.path.join(tmp_path, zip_file)
    print('update: INFO: create zip file \"' + os.path.relpath(zip_path, '.') + '\" ')
    
    import zipfile
    make_zip.make_zip_file(zip_path, flist, root_path, compress=zipfile.ZIP_DEFLATED)
    
    # compress done
    print('update: [ OK ] compress files done. ')

# make auto-pack zip file name
def make_re_pack_name():
    now = datetime.datetime.now()
    t = zero_len(now.year, 4) + '-'
    t += zero_len(now.month, 2) + '-'
    t += zero_len(now.day, 2) + '_'
    t += zero_len(now.hour, 2) + '-'
    t += zero_len(now.minute, 2) + '-'
    t += zero_len(now.second, 2)
    return t

def zero_len(n, l=2):
    t = str(int(n))
    while len(t) < l:
        t = '0' + t
    return t

# start from main
if __name__ == '__main__':
    main()

# end update_youtube_dl.py



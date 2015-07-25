# -*- coding: utf-8 -*-
# github.py for lieying_plugin
# o/update/github: gihub.com operations
# version 0.0.4.0 test201507251027

# import

import re
import urllib.request

# global vars

RE_LATEST_COMMIT = '\>latest commit \<span class\=\"sha\"\>([^\<]+)\</span>'

DL_BUFFER_SIZE = 16384	# 16 KB buffer size

# function

# get latest_commit sha str from github page
def get_latest_commit(html_text):
    m = re.findall(RE_LATEST_COMMIT, html_text)
    try:
        return m[0]
    except IndexError:
        return None	# get latest commit info failed

# https download for github

# simple download method, just return the content as text
def easy_dl(url):
    r = urllib.request.urlopen(url)
    raw = r.read()
    text = raw.decode('utf-8', 'ignore')
    return text

# save a large file to disk
def file_dl(url, fpath, buffer_size=DL_BUFFER_SIZE):
    
    # request http res
    r = urllib.request.urlopen(url)
    # count size
    count_byte = 0
    # open file and write content
    with open(fpath, 'wb') as f:
        while True:
            data = r.read(buffer_size)
            if not data:
                break
            f.write(data)
            # count byte
            count_byte += len(data)
    # save file done
    return count_byte

# end github.py



# -*- coding: utf-8 -*-
# entry.py for lieying_plugin/you-get (parse)
# plugin/plist/entry: parse video list entry file. 
# version 0.0.3.0 test201507131141

# import

import re

from urllib import request

from .site import list271

from ..tool.htmldom import htmldom

# global vars

URL_TO_SITE_LIST = {
    '^http://www.iqiyi.com/a_.+\.html' : list271, 
}

# base functions

def http_get(url):
    
    # make header
    header = {}
    header['Connection'] = 'close'
    
    req = request.Request(url, headers=header)
    res = request.urlopen(req)
    
    data = res.read()
    # just decode as utf-8
    t = data.decode('utf-8', 'ignore')
    # done
    return t

def get_site_module(url):
    m = None
    ulist = URL_TO_SITE_LIST
    for r in ulist:
        if re.match(r, url):
            m = ulist[r]
            break
    # done
    return m

# function

# check a input url is a list url
def check_is_list_url(url):
    rlist = URL_TO_SITE_LIST
    for r in rlist:
        if re.match(r, url):
            return True
    return False

# do parse video list
def parse_video_list(url):
    
    # get sub module
    list_entry = get_site_module(url)
    list_entry.htmldom = htmldom	# set import
    
    # load html_text
    html_text = http_get(url)
    # parse html_text and get info
    info = list_entry.get_list_info(html_text)
    
    # done
    return info

# end entry.py



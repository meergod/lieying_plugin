# -*- coding: utf-8 -*-
# tinfo.py for lieying_plugin/flvgo (parse)
# plugin/tinfo: translate info to plugin output format. 
# version 0.0.2.0 test201507132250

# import

import math

# global vars
DEFAULT_EXT = 'mp4'

# base functions

def get_flvgo_ext(raw_link):
    try:
        ext = raw_link.split('?', 1)[0].rsplit('.', 1)[1]
    except Exception:	# get ext from raw_link failed, use default ext
        ext = DEFAULT_EXT
    
    # done
    return ext

# add flvgo text size
def add_size(raw_list):
    
    unit_list = [
        'Byte', 
        'KB', 
        'MB', 
        'GB', 
        'TB', 
        'PB', 
        'EB', 
    ]
    
    slist = []	# size list
    # split number and unit
    for r in raw_list:
        rs = r.split(' ', 1)
        
        one = {}
        one['n'] = float(rs[0])
        
        # process unit
        try:
            one['u'] = unit_list.index(rs[1])
        except Exception:	# use unit as Byte
            one['u'] = 0
        
        slist.append(one)
    # add bytes
    count = 0
    for s in slist:
        one_byte = s['n'] * pow(1024, s['u'])
        if one_byte < 0:
            one_byte = 0
        count += int(one_byte)
    
    size_byte = count
    # make count byte to string
    size_str = byte2size(size_byte)
    
    # done
    return size_byte, size_str

def byte2size(size_byte):
    
    unit_list = [
        'Byte', 
        'KB', 
        'MB', 
        'GB', 
        'TB', 
        'PB', 
        'EB', 
    ]
    
    # get unit
    unit_i = math.floor(math.log(size_byte, 1024))
    unit = unit_list[unit_i]
    size_n = size_byte / pow(1024, unit_i)
    
    size_t = float_len(size_n)
    
    # make final size_str
    size_str = size_t + ' ' + unit
    # done
    return size_str

def float_len(n, l=1):
    
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

# clean before
def clean_before(text, to_clean=' \r\n	'):
    t = text
    while (len(t) > 0) and (t[0] in to_clean):
        t = t[1:]
    return t

# make label
def make_label(raw_info, time, split_char='：'):
    before = raw_info[0].split(split_char, 1)[1]
    after = clean_before(raw_info[1])
    
    label = before + '_' + after + '_' + time
    return label

# function

# pre process flvgo raw info
def pre_process(raw_info):
    raw = raw_info
    out = {}	# output info
    
    # add video info
    out['name'] = raw['name']
    out['site'] = raw['site']
    out['time'] = raw['time']
    
    # process formats
    out['data'] = []
    dlist = out['data']
    
    # process each format
    for data in raw['data']:
        one = {}
        
        # get ext
        ext = get_flvgo_ext(data['file'][0]['url'])
        one['ext'] = ext
        
        # make label
        label = make_label(data['label'], raw['time'])
        one['label'] = label
        
        size_list = []
        # add urls
        one['url'] = []
        for u in data['file']:
            one['url'].append(u['url'])
            size_list.append(u['size'])
        
        # process size
        size_byte, size_str = add_size(size_list)
        
        one['size_byte'] = size_byte
        one['size'] = size_str
        
        # get one format info done
        dlist.append(one)
    # get formats info done
    
    # sort formats by size
    dlist.sort(key=lambda x:x['size_byte'], reversed=False)
    
    # done
    return out

# export functions TODO

# translate for Parse() one video output
def t_format(raw_info):
    # TODO
    raw = raw_info
    out = {}	# output info
    
    out['type'] = 'formats'
    out['name'] = raw['title'] + '_' + raw['site']
    
    # only support one output format
    one = {}
    out['data'] = [one]
    
    # fix size string, MiB -> MB
    size = raw['size'].replace('iB', 'B', 1)
    one['size'] = size
    
    # get ext
    ext = get_you_get_ext(raw['type'])
    one['ext'] = ext
    
    # make label
    label = 'default_' + raw['type']
    one['label'] = label
    
    # done
    return out

# translate for ParseURL() output
def t_url(raw_info):
    # TODO
    raw = raw_info
    
    out = []
    # process each url, just add it
    for u in raw:
        one = {}
        one['protocol'] = 'http'
        one['args'] = {}
        one['value'] = u
        out.append(one)
    # done
    return out

# end tinfo.py



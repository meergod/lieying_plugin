# -*- coding: utf-8 -*-
# tinfo.py for lieying_plugin/flvgo (parse)
# plugin/tinfo: translate info to plugin output format. 
# version 0.0.1.0 test201507131525

# import

# global vars
DEFAULT_EXT = 'mp4'

# base functions

def get_flvgo_ext(raw_link):
    # TODO
    
    # get MIME format text
    mime = type_text.split('(', 1)[1].split(')', 1)[0]
    
    # use TYPE_TO_EXT_LIST to get ext
    ext = TYPE_TO_EXT_LIST[mime]
    
    return ext

# function

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



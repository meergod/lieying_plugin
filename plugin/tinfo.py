# -*- coding: utf-8 -*-
# tinfo.py for lieying_plugin/youtube-dl (parse)
# plugin/tinfo: translate info to plugin output format. 
# version 0.0.2.0 test201507221136

# import

# global vars

# base functions

# function

# TODO
# translate for Parse() one video output
def t_format(raw_info):
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



# -*- coding: utf-8 -*-
# parse_you_get.py for lieying_plugin/you-get (parse)
# plugin/parse_you_get: parse output text of you-get
# version 0.0.1.0 test201507131510

# base function

# clean chars before text
def clean_before(text, to_clean=' \r\n	'):
    t = text
    while (len(t) > 0) and (t[0] in to_clean):
        t = t[1:]
    return t

# function

# parse --info output
def parse_info(raw_text):
    
    raw = {}	# raw info
    
    fill_list = [
        'site', 
        'title', 
        'type', 
        'size', 
    ]
    # fill null info
    for f in fill_list:
        raw[f] = ''
    
    # cut text in lines
    line = raw_text.split('\n')
    
    # process key list
    key_list = {
        'Video Site' : 'site', 
        'Title' : 'title', 
        'Type' : 'type', 
        'Size' : 'size', 
    }
    
    # process each line
    for l in line:
        try:	# split may failed
            l0, l1 = l.split(':', 1)
        except Exception:
            continue	# just ignore this line
        
        for k in key_list:
            if l0 == k:
                raw[key_list[k]] = clean_before(l1)
    # process raw info done
    return raw

# parse --url output
def parse_url(raw_text):
    
    # get Real URLs part
    part = raw_text.split('Real URLs:', 1)
    
    # cut in lines
    line = part[1].split('\n')
    
    raw = []	# raw info
    
    # process each line
    for l in line:
        if l != '':	# check not null line
            raw.append(l)
    # parse raw done
    return raw

# end parse_you_get.py



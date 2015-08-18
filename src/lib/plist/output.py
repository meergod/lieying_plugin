# -*- coding: utf-8 -*-
# output.py for lyp_bridge/plist, lib/plist/output, sceext <sceext@foxmail.com> 
# version 0.0.2.0 test201508190250

# import
from ..easy import host_make_name

# functions

# translate info from plist raw parse output to lieying_plugin output format
def translate(raw_vlist):
    vlist = raw_vlist
    
    # make output info
    out = {}
    out['type'] = 'list'
    
    # add title
    out['title'] = vlist['title'] + '_' + vlist['site_name']
    
    # add data, video items, add each item
    out['data'] = []
    for i in range(len(vlist['list'])):
        raw = vlist['list'][i]
        one = {}
        out['data'].append(one)
        
        one['url'] = raw['url']
        one['no'] = raw['no']
        one['subtitle'] = raw['subtitle']
        
        # make name
        name = host_make_name.make_title(
        			title=vlist['title'] + raw['no'], 
        			title_sub=raw['subtitle'], 
        			title_no=(i + 1), 
        			title_short=vlist['title'], 
        			site_name=vlist['site_name'])
        # make name done
        one['name'] = name
    # add items done
    
    # done
    return out

# end output.py




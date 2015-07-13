# -*- coding: utf-8 -*-
# main.py for lieying_plugin/you-get (parse)
# plugin/main: plugin main file. 
# version 0.0.5.0 test201507131229

# import

import json

from . import version
from . import filter as filter0

from . import conf
from . import tinfo
from . import run_sub

from .plist import entry as plist
from .easy import host_make_name

from . import parse_you_get as parse0

# function

# parse more video
def parse_more(url):
    # parse video list
    vlist = plist.parse_video_list(url)
    
    # make output info
    out = {}
    out['type'] = 'list'
    out['more'] = False
    
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
    
    out['total'] = len(out['data'])
    # done
    return out

# parse one video
def parse_one(url):
    
    # NOTE load config here
    conf.load()
    
    # TODO
    pass

# lieying_plugin functions

def lieying_plugin_GetVersion():
    out = {}	# output info obj
    
    out['port_version'] = version.LIEYING_PLUGIN_PORT_VERSION
    out['type'] = version.LIEYING_PLUGIN_TYPE
    out['uuid'] = version.LIEYING_PLUGIN_UUID
    out['version'] = version.LIEYING_PLUGIN_VERSION
    
    out['name'] = version.make_plugin_name()
    out['filter'] = filter0.get_filter()
    
    out['author'] = version.THIS_AUTHOR
    out['license'] = version.THIS_LICENSE
    out['home'] = version.THIS_HOME
    out['note'] = version.THIS_NOTE
    
    # self define info
    out['pack_version'] = version.THIS_PACK_VERSION
    
    # done
    text = json.dumps(out)
    return text

def lieying_plugin_StartConfig():
    raise Exception('lieying_plugin/you-get: ERROR: [StartConfig()] not support config now. ')

def lieying_plugin_Parse(input_text):
    # check is video list
    if plist.check_is_list_url(input_text):
        info = parse_more(input_text)
    else:	# should use parse_one
        info = parse_one(input_text)
    # done
    text = json.dumps(info)
    return text

def lieying_plugin_ParseURL(url, label, i_min=None, i_max=None):
    
    # NOTE load config here
    conf.load()
    
    # TODO
    pass

# end main.py



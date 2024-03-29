# -*- coding: utf-8 -*-
# main.py for lieying_plugin/flvgo (parse)
# plugin/main: plugin main file. 
# version 0.0.9.0 test201507132302

# import

import json

from . import version
from . import filter as filter0

from . import conf
from . import tinfo
from . import http_request

from .plist import entry as plist
from .easy import host_make_name

from . import parse_flvgo as parse0

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
    
    # download flvgo html text
    flvgo_url = parse0.make_flvgo_url(url)
    try:
        html_text = http_request.http_get(flvgo_url)
    except Exception as e:
        raise Exception('plugin.main: ERROR: load flvgo html text failed. Please check the network. \"' + flvgo_url + '\"', e)
    
    # try to parse html_text
    try:
        raw_info = parse0.parse_html(html_text)
    except Exception as e:	# output error
        raise Exception('plugin.main: ERROR: [parse_flvgo.parse_html()] flvgo may get errors, please see <' + flvgo_url + '>', e)
    
    # try to translate info
    try:
        out = tinfo.t_format(raw_info)
    except Exception as e:	# output error
        raise Exception('plugin.main: ERROR: [tinfo.t_format()] flvgo may get errors, please see <' + flvgo_url + '>', e)
    
    # done
    return out


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
    raise Exception('lieying_plugin/flvgo: ERROR: [StartConfig()] not support config now. ')

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
    
    # NOTE now just ignore i_min, i_max
    # but NOT ignore label
    
    # download flvgo html text
    flvgo_url = parse0.make_flvgo_url(url)
    try:
        html_text = http_request.http_get(flvgo_url)
    except Exception as e:
        raise Exception('plugin.main: ERROR: load flvgo html text failed. Please check the network. \"' + flvgo_url + '\"', e)
    
    # try to parse html_text
    try:
        raw_info = parse0.parse_html(html_text)
    except Exception as e:	# output error
        raise Exception('plugin.main: ERROR: [parse_flvgo.parse_html()] flvgo may get errors, please see <' + flvgo_url + '>', e)
    
    # try to translate info
    try:
        out = tinfo.t_url(raw_info, label)
    except Exception as e:	# output error
        raise Exception('plugin.main: ERROR: [tinfo.t_url()] flvgo may get errors, please see <' + flvgo_url + '>', e)
    
    # done
    text = json.dumps(out)
    return text

# end main.py



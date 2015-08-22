# -*- coding: utf-8 -*-
# main.py for lyp_bridge, lib/main, sceext <sceext@foxmail.com> 
# version 0.1.2.0 test201508220923

# import

import os, json

from . import lyp_bridge as b
from . import conf, cache

from .nosalt import get_nosalt

from .plist import entry as plist
from .plist import output as plisto

# global vars
PACK_VERSION = 5

FILTER_DEFAULT = [	# default filter info for lieying_plugin
    '^http://.+', 
]

ly_root_path = ''	# lieying root path, used to fix sub_domain_base_path

# functions

# make root path
def make_root_path():
    # from C:\Program Files (x86)\LieYing\Data\Plugins\_EA078240_D566_42BC_A9FD_2F5B5FBBCD8B
    # to C:\Program Files (x86)\LieYing
    rel_path = '../../../../'
    plugin_dir = os.path.normpath(os.path.dirname(__file__))
    r_path = os.path.normpath(os.path.join(plugin_dir, rel_path))
    # FIXME tmp fix here
    # NOTE fix bug here, add '\\' after r_path
    if not r_path.endswith('\\'):
        r_path += '\\'
    # save path
    global ly_root_path
    ly_root_path = r_path
    return r_path	# done

# custom version info
def make_version(raw_info):
    raw = json.loads(raw_info)
    
    # version info by lyp_bridge
    ver = {
        'port_version' : '0.3.0-test.8', 
        'uuid' : '9eb959fe-36e5-4d0c-88c6-fd779254b4ee', 
        'version' : '0.5.0', 
        
        'author' : 'sceext <sceext@foxmail.com>', 
        'license' : 'unlicense <http://unlicense.org/>', 
        'home' : 'https://github.com/sceext2/lieying_plugin', 
        'note' : 'A lieying python3 plugin, use lyp_bridge to provide functions of piaopiao wuyan programs. \n With wuyan2 : C# WebBrowser + node.js enhp http proxy server to get target key url. ', 
        'pack_version' : PACK_VERSION, 
    }
    
    # update args from raw
    out = raw.copy()
    out['uuid'] = ver['uuid']	# replace uuid to this plugin
    out['version'] = ver['version'] + '_' + raw['version']	# mix version str
    out['pack_version'] = ver['pack_version']	# add more info
    out['port_version'] = ver['port_version']	# reset port_version
    # remove copyright
    if 'copyright' in out:
        out.pop('copyright')
    
    # update each multi-line values
    update_list = [
        'author', 
        'license', 
        'home', 
        'note', 
    ]
    for i in update_list:
        if i in out:
            out[i] = ver[i] + '\n' + raw[i]
        else:
            out[i] = ver[i]
    
    # try to add filter
    if not 'filter' in out:
        out['filter'] = FILTER_DEFAULT
    
    # make plugin name
    raw_name = [
        'lyp_bridge-wuyan2-wbnp-(', 
        ' 外挂) ', 
        ' version ', 
    ]
    
    name = raw_name[0] + raw['name'] + raw_name[1]
    name += str(ver['pack_version']) + raw_name[2]
    name += out['version'] + ' [sceext] '
    out['name'] = name
    
    # done
    text = json.dumps(out)
    return text

# use get_nosalt before call sub to parse
def make_nosalt(url):
    raw = get_nosalt.get_info(url)
    # get info from raw
    info = raw['url']
    # write info with cache
    cache.update(url, info)
    # done

# exports functions

def GetVersion(*k, **kw):
    b.start(ly_root_path)
    raw = b.GetVersion(*k, **kw)
    b.exit()	# NOTE exit after GetVersion(), FIX a BUG here
    
    # modify version info
    r = make_version(raw)
    return r

def Config(*k, **kw):
    b.start(ly_root_path)
    return b.Config(*k, **kw)

def Update(*k, **kw):
    b.start(ly_root_path)
    return b.Update(*k, **kw)

def Parse(*k, **kw):
    url = k[0]	# get args
    
    # check to parse plist
    if plist.check_is_list_url(url):
        # parse plist
        raw_info = plist.parse_video_list(url)
        # translate it to lieying_plugin output format
        out = plisto.translate(raw_info)
        # parse plist done
        text = json.dumps(out)
        return text
    else:	# use normal parse
        # check config flag
        if conf.enable_nosalt:
            make_nosalt(url)
        # use sub to really parse
        b.start(ly_root_path)
        return b.Parse(*k, **kw)
    # parse function done

def ParseURL(*k, **kw):
    if conf.enable_nosalt:
        url = k[0]
        # FIXME the first URL may be never out-of-data now, so no need to make again
        #make_nosalt(url)
    # use sub to really parse
    b.start(ly_root_path)
    return b.ParseURL(*k, **kw)

# export for DEBUG
p = b.p

# end main.py



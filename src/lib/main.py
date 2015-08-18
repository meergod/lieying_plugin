# -*- coding: utf-8 -*-
# main.py for lyp_bridge, lib/main, sceext <sceext@foxmail.com> 
# version 0.0.1.0 test201508190015

# import

import os, json

from . import lyp_bridge as b
from . import conf, cache

from .nosalt import get_nosalt

# global vars
PACK_VERSION = 2

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
        'port_version' : '0.3.0-test.7', 
        'uuid' : '2280f81b-7447-47e2-b7a8-3f760f8fa62b', 
        'version' : '0.2.0', 
        
        'author' : 'sceext <sceext@foxmail.com>', 
        'license' : 'unlicense <http://unlicense.org/>', 
        'home' : 'https://github.com/sceext2/lieying_plugin/tree/lyp_bridge-pp-wuyan', 
        'note' : 'A lieying python3 plugin, use lyp_bridge to provide functions of piaopiao wuyan programs. ', 
        'pack_version' : PACK_VERSION, 
    }
    
    # update args from raw
    out = raw.copy()
    out['uuid'] = raw['uuid']	# replace uuid from raw
    out['version'] = ver['version'] + '_' + raw['version']	# mix version str
    out['pack_version'] = ver['pack_version']	# add more info
    
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
        'lyp_bridge-wuyan-pp-', 
        ' version ', 
    ]
    
    name = raw_name[0] + raw['name'] + ' '
    name += str(ver['pack_version']) + raw_name[1]
    name += out['version'] + ' [sceext] '
    out['name'] = name
    
    # done
    text = json.dumps(out)
    return text

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
    b.start(ly_root_path)
    return b.Parse(*k, **kw)

def ParseURL(*k, **kw):
    b.start(ly_root_path)
    return b.ParseURL(*k, **kw)

# export for DEBUG
p = b.p

# end main.py



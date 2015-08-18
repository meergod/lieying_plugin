# -*- coding: utf-8 -*-
# run.py for lyp_bridge, lieying_plugin python3 to C# .net bridge, sceext <sceext@foxmail.com> 
# version 0.0.3.0 test201508181842

# import

import json

# NOTE try to fix import
try:
    from . import lyp_bridge as b
except Exception:
    import lyp_bridge as b

# global vars
PACK_VERSION = 1

FILTER_DEFAULT = [	# default filter info for lieying_plugin
    '^http://.+', 
]

# functions

# custom version info
def make_version(raw_info):
    raw = json.loads(raw_info)
    
    # version info by lyp_bridge
    ver = {
        'port_version' : '0.3.0-test.7', 
        'uuid' : '2280f81b-7447-47e2-b7a8-3f760f8fa62b', 
        'version' : '0.1.0', 
        
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
        out['filter'] = FILTER_DEFUALT
    
    # make plugin name
    raw_name = [
        'lyp_bridge-sceext-pp-wuyan-', 
        ' version ', 
    ]
    
    name = raw_name[0] + raw['name'] + ' '
    name += str(ver['pack_version']) + raw_name[1]
    name += out['version'] + '('
    name += out['license'] + ') '
    out['name'] = name
    
    # done
    text = json.dumps(out)
    return text

# exports functions

def GetVersion(*k, **kw):
    b.start()
    raw = b.GetVersion(*k, **kw)
    b.exit()	# NOTE exit after GetVersion(), FIX a BUG here
    
    # modify version info
    r = make_version(raw)
    return r

def Config(*k, **kw):
    b.start()
    return b.Config(*k, **kw)

def Update(*k, **kw):
    b.start()
    return b.Update(*k, **kw)

def Parse(*k, **kw):
    b.start()
    return b.Parse(*k, **kw)

def ParseURL(*k, **kw):
    b.start()
    return b.ParseURL(*k, **kw)

p = b.p

# end run.py



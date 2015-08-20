# -*- coding: utf-8 -*-
# run.py for lyp_bridge, lieying_plugin python3 to C# .net bridge, sceext <sceext@foxmail.com> 
# version 0.0.2.1 test201508180134

# import

# NOTE try to fix import
try:
    from . import lyp_bridge as b
except Exception:
    import lyp_bridge as b

# functions

# exports functions

def GetVersion(*k, **kw):
    b.start()
    r = b.GetVersion(*k, **kw)
    b.exit()	# NOTE exit after GetVersion(), FIX a BUG here
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



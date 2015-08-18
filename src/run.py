# -*- coding: utf-8 -*-
# run.py for lyp_bridge, lieying_plugin python3 to C# .net bridge, sceext <sceext@foxmail.com> 
# version 0.1.0.0 test201508190321

# import

# NOTE try to fix import
try:
    from .lib import main
except Exception:
    from lib import main

# functions

# exports functions, just call functions in main.py
GetVersion = main.GetVersion
Config = main.Config
# NOTE not support Update function now
#Update = main.Update
Parse = main.Parse
ParseURL = main.ParseURL

# export for DEBUG
p = main.p

# set ly_root_path at init
main.make_root_path()

# end run.py



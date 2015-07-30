# -*- coding: utf-8 -*-
# run.py for lieying_plugin/module-update (plugin)
# run: lieying_plugin entry file. 
# version 0.0.1.0 test201507301823

# import

import os
import sys
import json

# try normal import, import plugin.main
try:
    from .plugin import main
except Exception as e:
    print('import main ERROR ' + str(e))
    # try to import for DEBUG
    sys.path.insert(0, os.path.dirname(__file__))
    from plugin import main
# import done

# exports functions for lieying_plugin port_version 0.3.0

GetVersion = main.lieying_plugin_GetVersion		# GetVersion()
# StartConfig = main.lieying_plugin_StartConfig		# StartConfig()
Update = main.lieying_plugin_Update			# Update(local_path='')


# exports functions for other plugins to use
# TODO

# NOTE add p() function for DEBUG
def p(o):
    print(json.dumps(json.loads(o), indent=4, sort_keys=True, ensure_ascii=False))

# end run.py



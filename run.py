# -*- coding: utf-8 -*-
# run.py for lieying_plugin/module-update (plugin)
# run: lieying_plugin entry file. 
# version 0.0.2.0 test201508041714

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
easy_update = main.easy_update		# easy_update(local_path='', plugin_uuid=None, conf=None)
update_local = main.update_local	# update_local(local_path='', plugin_uuid=None, conf=None)
update_network = main.update_network	# update_network(plugin_uuid=None, conf=None)


# NOTE add p() function for DEBUG
def p(o):
    print(json.dumps(json.loads(o), indent=4, sort_keys=True, ensure_ascii=False))

# end run.py



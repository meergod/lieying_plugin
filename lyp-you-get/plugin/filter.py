# -*- coding: utf-8 -*-
# filter.py for lieying_plugin/you-get (parse)
# plugin/filter: define filter for GetVersion()
# version 0.0.2.0 test201507131538

# global vars

LIEYING_PLUGIN_FILTER = [
    '^http://.+\.iqiyi\.com/.+', 
]

# function
def get_filter():
    # no more to do, just return it
    return LIEYING_PLUGIN_FILTER

# end filter.py



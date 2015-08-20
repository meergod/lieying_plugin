# -*- coding: utf-8 -*-
# filter.py for lieying_plugin/flvgo (parse)
# plugin/filter: define filter for GetVersion()
# version 0.0.3.0 test201507131952

# global vars

LIEYING_PLUGIN_FILTER = [
    '^http://.+', 
]

# function
def get_filter():
    # no more to do, just return it
    return LIEYING_PLUGIN_FILTER

# end filter.py



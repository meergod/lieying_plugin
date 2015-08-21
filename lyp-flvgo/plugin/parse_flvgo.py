# -*- coding: utf-8 -*-
# parse_flvgo.py for lieying_plugin/flvgo (parse)
# plugin/parse_flvgo: parse html text of flvgo
# version 0.0.4.0 test201507132216

# import

import urllib.parse

from .tool.htmldom import htmldom

from . import conf

# base function

# function

# make flvgo url
def make_flvgo_url(url):
    # load config first
    conf.load()
    
    base_url = conf.etc['flvgo_url']
    
    full_url = base_url + urllib.parse.quote(url, safe='')
    # done
    return full_url

def parse_html(html_text):
    # parse html with htmldom
    dom = htmldom.HtmlDom()
    root = dom.createDom(html_text)
    
    out = {}	# output info
    
    # get video info
    vinfo = root.find('div.video-info')[0]
    
    # get video name
    vname = vinfo.find('h2 span.name')[0].text()
    out['name'] = vname
    
    vinfoli = vinfo.find('ul li strong')
    # get site, and video time
    site = vinfoli[0].text()
    time = vinfoli[2].text()
    out['site'] = site
    out['time'] = time
    
    # get download info block
    vdown = root.find('div.result-down')[0]
    
    # get format blocks
    vfname = vdown.find('h4')	# format name title
    vurl = vdown.find('table')	# format download url info
    
    # process each format
    flist = []
    out['data'] = flist
    
    # NOTE fix vurl here
    vurl = vurl[1::2]
    
    # check page struct
    if vfname.len != vurl.len:
        raise Exception('parse_flvgo: ERROR: page struct error, vfname.len ' + str(vfname.len) + ', vurl.len ' + str(vurl.len))
    
    # process each format
    for i in range(vurl.len):
        now_name = vfname[i]
        now_url = vurl[i]
        
        one = {}
        
        label = now_name.text()
        # simple process label text
        label = label.split('\n')[:2]
        one['label'] = label
        
        # get files info
        one['file'] = []
        onef = one['file']
        
        # process each file
        urls = now_url.find('tr')[1:]	# first tr is title, remove it
        for uinfo in urls:
            one_file = {}
            # get one file info
            
            tds = uinfo.find('td')
            # get index for debug
            one_file['index'] = tds[0].text()
            # get size text
            one_file['size'] = tds[1].text()
            
            # get url
            url_a = tds[2].find('a')[0].attr('href')
            one_file['url'] = url_a
            
            # get one file info done
            onef.append(one_file)
        # get one format info done
        flist.append(one)
    # get flvgo info done
    
    return out

# end parse_flvgo.py



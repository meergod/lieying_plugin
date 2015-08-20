# -*- coding: utf-8 -*-
# list271.py for lieying_plugin/you-get (parse)
# plugin/plist/site/list271: parse video list of 271. 
# version 0.0.8.0 test201507131137

# import

# NOTE should be set
htmldom = None	# python htmldom parse html module

# function

def get_list_info(html_text):
    # parse html_text with htmldom
    dom = htmldom.HtmlDom()
    root = dom.createDom(html_text)
    
    # get block
    blocks = root.find('ul.site-piclist[data-albumlist-elem=cont]')
    block = blocks[0]
    
    # get some list
    a_list = block.find('a.site-piclist_pic_link')
    url_list = []
    title_list = []
    for a in a_list:
        url_list.append(a.attr('href'))
        title_list.append(a.attr('title'))
    
    ns = block.find('p.site-piclist_info_title>a')
    
    # NOTE fix ns here
    ns = ns[::2]
    
    n_list = []
    for n in ns:
        n_list.append(n.text())
    
    # get album name
    album_a = root.find('div.crumb-item a')
    album_name = album_a[-1].text()
    
    # make output info obj
    info = {}
    info['list'] = []
    for i in range(len(url_list)):
        one = {}
        info['list'].append(one)
        
        one['url'] = url_list[i]
        one['subtitle'] = title_list[i]
        one['no'] = n_list[i]
    
    # add album_name
    info['title'] = album_name
    
    # clean album_name
    while info['title'][-1] in '\r\n':
        info['title'] = info['title'][:-1]
    # add site name
    info['site_name'] = '不可说'
    
    # done
    return info

# end list271.py



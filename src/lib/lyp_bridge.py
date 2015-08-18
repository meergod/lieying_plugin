# -*- coding: utf-8 -*-
# lyp_bridge.py, a bridge from python3 to .net C# lieying_plugin .dll, sceext <sceext@foxmail.com>
# version 0.1.4.0 test201508190018

# import

import os, sys, json
import subprocess

from . import io_one_line_only as ioo

# global vars

etc = {}	# global conf info
etc['bin_exe'] = '../lyp_bridge.exe'	# path from now_dir
etc['p'] = None	# subprocess.Popen() object

# path from now_dir
etc['dll_name'] = '../../_EA078240_D566_42BC_A9FD_2F5B5FBBCD8B/Run.dll'

# to fix sub pass args
etc['fix_parse_url_i_min'] = 0
etc['fix_parse_url_i_max'] = 1048576

# NOTE fix line-end
LINE_END = '\r\n'
# NOTE fix sub-encoding
#SUB_ENCODING = ['utf-8', 'utf-8']	# fix for stdin and stdout
# FIXME tmp fix, NOTE fix on windows
SUB_ENCODING = ['cp936', 'cp936']

# functions

# fix bad json text
def fix_bad_json1(raw):
    out = ''
    # scan full text, and make string from '' to ""
    flag_in = None	# in '' or out ''
    flag_s = False	# after \ char
    for c in raw:
        # check in flag first
        if flag_in != None:
            # check s flag
            if flag_s:	# just append this char
                flag_s = False
            else:	# check out flag
                if c == flag_in:
                    flag_in = None	# clear in flag
                    out += '\"'	# add stand out char
                    continue	# not append the raw char
        else:	# check in flag
            if c in '\'\"':
                flag_in = c	# turn on in flag
                out += '\"'	# add stand in char
                continue	# not add the raw char
        # default action, append the char
        out += c
    # process string done
    return out

# base functions

# get sub output
def get_sub_out():
    p = etc['p']
    # NOTE fix encoding BUG, get encoding
    encoding = SUB_ENCODING[1]
    # get sub one line output
    raw = p.stdout.readline().decode(encoding)
    # remove \n after raw
    if raw.endswith('\n'):
        raw = raw[:-len('\n')]
    elif raw.endswith('\r\n'):
        raw = raw[:-len('\r\n')]
    elif raw.endswith('\r'):
        raw = raw[:-len('\r')]
    # decode sub output to get info
    i = ioo.decode(raw)
    # done
    return i

# send a command to sub
def send_to_sub(c, line_end=LINE_END):
    text = ioo.encode(c) + line_end
    p = etc['p']
    # NOTE fix encoding BUG, get encoding
    encoding = SUB_ENCODING[0]
    p.stdin.write(bytes(text, encoding))
    # NOTE flush after write, to fix BUG
    p.stdin.flush()
    # done

# sub_do, send a command to sub and get result
def sub_do(c):
    # send command to sub
    send_to_sub(c)
    while True:	# support many print
        # get result
        result = get_sub_out()
        # check sub 'print' request and support it
        if result[0] == 'print':
            print(result[1])	# just print it
        elif result[0] != '':	# check ERROR
            raise Exception('ERROR: sub return error', result[0], result[1])
        else:	# sub OK
            return result[1:]	# remove first args
    # done

# really start sub
def real_start(domain_path=''):
    # get bin file path
    now_dir = os.path.abspath(os.path.dirname(__file__))
    bin_file = os.path.normpath(os.path.join(now_dir, etc['bin_exe']))
    # make dll path
    dll_file = os.path.normpath(os.path.join(now_dir, etc['dll_name']))
    # make args
    arg = [bin_file, dll_file]
    # check domain_path
    if domain_path != '':
        arg += [domain_path, bin_file]
    # create sub process
    PIPE = subprocess.PIPE
    p = subprocess.Popen(arg, stdin=PIPE, stdout=PIPE, stderr=sys.stderr, shell=False)
    etc['p'] = p
    # wait until sub successfully started
    i = get_sub_out()
    if i[0] == '':	# check sub started OK
        return i[1]	# started OK
    else:	# start ERROR
        raise Exception('ERROR: ' + i[0] + ': ' + str(i[1:]))
    # real start done

# export functions

# start sub process
def start(domain_path=''):
    # check now status
    if (etc['p'] == None) or (etc['p'].poll() != None):
        # sub is not running
        return real_start(domain_path)	# do start it
    else:	# sub is running
        return 'WARNING: sub is already running. '
    # check and start sub done

# exit sub process
def exit():
    # send exit command
    send_to_sub(['exit'])
    # wait and get exit_code
    p = etc['p']
    exit_code = p.wait()
    # clean p and done
    etc['p'] = None
    return exit_code

# functions exports by sub

# GetVersion
def GetVersion():
    r = sub_do(['GetVersion'])
    # FIXME fix sub output, fix the bad json text
    bad = str(r[0])
    good = fix_bad_json1(bad)
    return good

# Config(show_window=False)
def Config(show_window=False):
    # check args
    if show_window:	# should call sub's Config()
        sub_do(['Config'])
    else:	# should call sub's ApplyConfig()
        sub_do(['ApplyConfig'])
    # process done

# Update(local_path='')
def Update(local_path=''):
    local_path = str(local_path)
    r = sub_do(['Update', local_path])
    return str(r[0])

# Parse(url)
def Parse(url):
    url = str(url)
    r = sub_do(['Parse', url])
    return str(r[0])

# ParseURL(url, label, i_min=None, i_max=None)
def ParseURL(url, label, i_min=None, i_max=None):
    # process args
    if i_min == None:
        i_min = etc['fix_parse_url_i_min']
    if i_max == None:
        i_max = etc['fix_parse_url_i_max']
    i_min = int(i_min)
    i_max = int(i_max)
    
    url = str(url)
    label = str(label)
    i_min = str(i_min)
    i_max = str(i_max)
    
    r = sub_do(['ParseURL', url, label, i_min, i_max])
    return str(r[0])

# TODO NOTE not support Search() now

# p function is for DEBUG
def p(o):
    print(json.dumps(json.loads(o), indent=4, sort_keys=True, ensure_ascii=False))

# end lyp_bridge.py



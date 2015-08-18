# -*- coding: utf-8 -*-
# io_one_line_only.py, pass many text in only one line text, sceext <sceext@foxmail.com> 
# version 0.0.4.0 test201508160535

# import

# global vars

# functions

# io encode function
def encode(raw_text_list=[]):
    raw = raw_text_list.copy()
    # check null list
    if len(raw) < 1:
        return ''
    # pre-process each raw text
    for i in range(len(raw)):
        t = raw[i]
        # process this text
        
        # keep all '\' chars to be safe
        t = t.replace('\\', '\\\\')
        # NOTE fix '\r', or '\r\n'
        t = t.replace('\r\n', '\n')
        t = t.replace('\r', '\n')
        # process multi-lines text
        t = t.replace('\n', '\\n')
        
        # process one text done
        raw[i] = t
    # join all text to finish encode
    out = ('\\0').join(raw)
    out += '\\0'	# add one more \0 after last line
    # done
    return out

# io decode function
def decode(raw_text=''):
    # check null decode
    if raw_text == '':
        return []
    # normal decode, should scan each char
    out = []
    flag_ = False
    t = ''
    for c in raw_text:
        # check flag
        if flag_:
            flag_ = False	# turn off flag first
            # check chars
            if c == '\\':
                t += '\\'	# should be \ char
            elif c == 'n':	# should be '\n' char
                t += '\n'
            elif c == '0':	# \0, should start a new text
                out.append(t)
                t = ''	# reset text
            else:	# as a normal char
                t += c
        else:	# check set flag
            if c == '\\':
                flag_ = True	# should turn on flag
            else:
                t += c	# append as a normal char
    # NOTE do not add last line
    return out	# done


# test functions

# exit command is ':exit'
def test_encode(flag_decode=False):
    # import for debug
    import json
    
    exit_c = ':exit'
    # test until got exit command
    while True:
        # get input
        i = []
        # get input until got start test command
        start_c = ':test'
        while True:
            one = input(':')
            if one == start_c:
                break
            elif one == exit_c:	# check exit command
                return
            i.append(one)
        # just start test
        result = encode(i)
        # print result
        print(result)
        # check if should auto-test decode
        if flag_decode:
            print(':: auto-test decode')
            test = decode(result)
            # print result and compare auto
            before = json.dumps(i, indent=4, ensure_ascii=False)
            after = json.dumps(test, indent=4, ensure_ascii=False)
            _ok = (before == after)
            print(before + '\n' + after + '\n:: result ' + str(_ok))
    # test done

# exit command is ':exit-decode'
def test_decode():
    
    # import for debug
    import json
    
    exit_c = ':exit-decode'
    while True:
        # get input, just one line
        i = input(':')
        # check exit command
        if i == exit_c:
            return
        # start test and print result
        result = decode(i)
        text = json.dumps(result, indent=4, ensure_ascii=False)
        print(text + '\n')
    # test done

# end io_one_line_only.py



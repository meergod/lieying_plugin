# -*- coding: utf-8 -*-
# make_zip.py for lieying_plugin/module-update (plugin)
# plugin/update/make_zip: read and write zip files. 
# version 0.0.10.0 test201508071435

# import
import os
import zipfile

# function

# add files of a list to a zip file
def make_zip_file(output_file, file_list=[], base_path='.', compress=zipfile.ZIP_DEFLATED, mode='w', path_before=None):
    
    with zipfile.ZipFile(output_file, mode=mode, compression=compress, allowZip64=True) as z:
        for f in file_list:
            fpath = os.path.join(base_path, f['name'])
            # check and add path_before
            to_path = f['name']
            if path_before and (path_before != None) and (path_before != ''):
                to_path = os.path.join(path_before, to_path)
            z.write(fpath, arcname=to_path)
    # create zip file done

# get file list in a zip file
def get_file_list(zip_file):
    out = {}
    out['list'] = []
    flist = out['list']
    
    count_size = 0
    count_zsize = 0
    
    with zipfile.ZipFile(zip_file) as z:
        ilist = z.infolist()	# info list
        for i in ilist:
            one = {}
            # file name
            one['name'] = i.filename
            # file size
            one['size'] = i.file_size
            # compressed size
            one['zsize'] = i.compress_size
            # count size
            count_size += one['size']
            count_zsize += one['zsize']
            
            flist.append(one)
    # get file list done
    out['count'] = len(flist)
    out['size'] = count_size
    out['zsize'] = count_zsize
    # done
    return out

# extract a zip file to a given path with a file list
def extract_zip_file(zip_file, file_list=[], base_path='.'):
    
    with zipfile.ZipFile(zip_file) as z:
        for f in file_list:
            z.extract(f['name'], path=base_path)
    # extract zip file done

# end make_zip.py



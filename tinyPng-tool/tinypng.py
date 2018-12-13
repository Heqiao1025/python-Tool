#! /usr/bin/python
# -*- coding: UTF-8 -*-

import tinify
import os
import shutil
import filetype

#上传图片大小最小20kb，可以人为降低或升高，但不可以超过最大基数
upload_file_size_min = 200000
#上传图片大小最大5MB, 不可以人为改变
upload_file_size_max = 5000000
#上传图片最大数量，如果付费用户可随意更改。。。。。。
upload_file_max = 500

#所有待替换image文件
image_files = []
image_file_paths = []

replace_Old_Path = ''
replace_New_Path = ''



def tinifyUploadFile(image_path_root ,image_file):
    global replace_Old_Path, replace_New_Path
    tinify.key = 'FJ71q0DM0nQGDTZ3LT818XLTcHSK134Q'
    new_image_path_root = image_path_root.replace(replace_Old_Path, replace_New_Path)
    if (os.path.exists(new_image_path_root) == False):
        os.makedirs(new_image_path_root)

    rs = False
    try:
        source = tinify.from_file(os.path.join(image_path_root, image_file))
        source.to_file(os.path.join(new_image_path_root, image_file))
        rs = True
    except tinify.AccountError, e:
        print "The error message is: %s" % e.message
    except tinify.ServerError, e:
        print "The error message is: %s" % e.message
        pass
    except tinify.ConnectionError, e:
        print "The error message is: %s" % e.message
        pass
    except Exception, e:
        print "The error message is: %s" % e.message
        pass
    return rs

def newImageRootPath(old_image_path_root):
    pathList = old_image_path_root.split('/')
    pathList.pop(-1)
    pathList.pop(0)
    new_image_path_root = ''
    for pathName in pathList:
        new_image_path_root += '/' + pathName
    return new_image_path_root + '/tinifyNewImages'

def imageFiles():
    global replace_Old_Path, image_files, image_file_paths
    for root, folders, files in os.walk(replace_Old_Path):
        for file in files:
            if (os.path.getsize(os.path.join(root, file)) < upload_file_size_min) and  (os.path.getsize(os.path.join(root, file)) > upload_file_size_max):
                continue
            kind = filetype.guess(os.path.join(root, file))
            if kind is None:
                continue
            if (kind.extension is 'jpg') or (kind.extension is 'png'):
                if tinifyUploadFile(root, file) == True:
                    print os.path.join(root, file) + '😊😊😊😊😊😊😊'
                else:
                    print os.path.join(root, file) + '😭😭😭😭😭😭😭'
            else:
                continue
    print "压缩完毕"

def replacePath():
    global replace_Old_Path, replace_New_Path
    while 1:
        replace_Old_Path = raw_input("将文件路径⬇️⬇️⬇️⬇️⬇️⬇️\n")
        if (os.path.exists(replace_Old_Path) == False):
            print '文件路径🙅🙅🙅🙅🙅🙅‍'
        else:
            replace_New_Path = newImageRootPath(replace_Old_Path)
            if (os.path.exists(replace_New_Path) == False):
                os.makedirs(replace_New_Path)
            else:
                raw_input("将要覆盖原压缩文件，回车继续")

                shutil.rmtree(replace_New_Path)
                # image_roots = []
                # for root, floders, files in os.walk(replace_New_Path):
                #     for file in files:
                #         os.remove(os.path.join(root, file))
                #     image_roots.append(root)
                #
                # os.remove(replace_New_Path)
            break

if __name__ == "__main__":
    replacePath()
    imageFiles()
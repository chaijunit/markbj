#coding:utf-8
import os
import re
import uuid
import shutil
from flask import current_app 


# 匹配文件类型
reg = re.compile(r'\w+\.(bmp|gif|jpeg|png|jpg)$', re.I|re.U) # re.I 是忽略大小写 re.U 使用Unicode库


def validate_image(filename):
    dir, name = os.path.split(filename)
    if dir or not reg.search(name):
        return False
    return True


def generate_tmpfile(file):
    """
    生成文件
    @file: 文件对象
    """
    u = uuid.uuid1()
    name, ext = os.path.splitext(file.filename)
    _filename = ''.join([u.hex, ext])
    path = '/'.join(['', current_app.config["TMP_PATH"], _filename])
    tmp_path = ''.join([current_app.root_path, path])
    file.save(tmp_path)
    return (path, name)


def enable_tmpfile(dest_path, filename):
    """
    激活缓存文件
    @dest_path: 移动相对目的路径
    @filename: 文件名
    """
    tmp_path = current_app.config["TMP_PATH"]
    tmp_file = '/'.join([current_app.root_path, tmp_path, filename])
    if not os.path.exists(tmp_file):
        return False
    dest_file = '/'.join([current_app.root_path, dest_path, filename])
    shutil.move(tmp_file, dest_file)
    return True


def remove_tmpfile(filename):
    """
    删除缓存文件
    @filename: 文件名
    """
    tmp_path = current_app.config["TMP_PATH"]
    return remove_file(tmp_path, filename)
    

def remove_file(path, filename):
    """
    删除文件
    @path: 相对路径
    @filename: 文件名
    """
    full_file = '/'.join([current_app.root_path, path, filename])
    if not os.path.exists(full_file):
        return False
    print 'remove_file', full_file
    os.remove(full_file)
    return True



#coding: utf-8
import os
import uuid
import shutil
from PIL import Image
import StringIO
from flask import current_app
from .upload_file import  remove_file

def generate_origin_avatar(name, im):
    """ 生成原始大小的头像 """
    avatar_image = "/".join([current_app.root_path, 
        current_app.config["AVATAR_IMAGE_PATH"], name])
    im.save(avatar_image)


def generate_thumbnail_avatar(name, im):
    """ 生成128*128大小的头像 """
    name = "thumbnail_{0}".format(name)
    avatar_image = "/".join([current_app.root_path, 
        current_app.config["AVATAR_IMAGE_PATH"], name])
    _im = im.resize((128,128), Image.ANTIALIAS)
    _im.save(avatar_image)


def generate_50px_avatar(name, im):
    """ 生成50*50大小的头像 """
    name = "50_50_{0}".format(name)
    avatar_image = "/".join([current_app.root_path, 
        current_app.config["AVATAR_IMAGE_PATH"], name])
    _im = im.resize((50, 50), Image.ANTIALIAS)
    _im.save(avatar_image)
 

def generate_20px_avatar(name, im):
    """ 生成 20*20 大小的头像 """
    name = "20_20_{0}".format(name)
    avatar_image = "/".join([current_app.root_path, 
        current_app.config["AVATAR_IMAGE_PATH"], name])
    _im = im.resize((20, 20), Image.ANTIALIAS)
    _im.save(avatar_image)


def init_avatar():
    common_image = '/'.join([current_app.root_path, 
        current_app.config["IMG_PATH"],
        "blue.jpg"])
    u = uuid.uuid1()
    name = '{0}.jpg'.format(u.hex)
    im = Image.open(common_image)
    generate_origin_avatar(name, im)
    generate_thumbnail_avatar(name, im)
    generate_20px_avatar(name, im)
    generate_50px_avatar(name, im)
    return name
 

def remove_avatar(name):
    """ 删除头像 """
    thumbnail_image = 'thumbnail_{0}'.format(name)
    remove_file(current_app.config["AVATAR_IMAGE_PATH"], name)
    remove_file(current_app.config["AVATAR_IMAGE_PATH"], thumbnail_image)
    remove_file(current_app.config["AVATAR_IMAGE_PATH"], "20_20_{0}".format(name))
    remove_file(current_app.config["AVATAR_IMAGE_PATH"], "50_50_{0}".format(name))
   

def change_avatar(binary, old_avatar):
    """ 改变头像 """
    u = uuid.uuid1()
    name = '{0}.png'.format(u.hex)
    im = Image.open(StringIO.StringIO(binary))
    generate_origin_avatar(name, im)
    generate_thumbnail_avatar(name, im)
    generate_20px_avatar(name, im)
    generate_50px_avatar(name, im)
    remove_avatar(old_avatar)
    return name


def remove_cover(filename):
    """ 删除封面 """
    thumbnail_image = 'thumbnail_{0}'.format(filename)
    remove_file(current_app.config["COVER_IMAGE_PATH"], filename)
    remove_file(current_app.config["COVER_IMAGE_PATH"], thumbnail_image)
   

def change_cover(binary, old_cover):
    u = uuid.uuid1()
    name = "{0}.png".format(u.hex)
    cover_image = '/'.join([current_app.root_path, 
        current_app.config["COVER_IMAGE_PATH"], name])
    im = Image.open(StringIO.StringIO(binary))
    im.save(cover_image)
    im.thumbnail((320, 80), Image.ANTIALIAS)
    thumbnail_image = 'thumbnail_{0}'.format(name)
    thumbnail_image= '/'.join([current_app.root_path, 
        current_app.config["COVER_IMAGE_PATH"], thumbnail_image])
    im.save(thumbnail_image)
    if old_cover:
        remove_cover(old_cover)
    return name
    


#coding: utf-8

from flask import current_app, request
from flask.ext.login import current_user
import base64
import random
from app.home.models import User
from app.common.upload_file import *
from app.common import avatar
from app.common.ajax import *


def change_avatar(binary = None, *args, **kwargs):
    if not binary:
        return message("error", "", "数据有误")
    binary = base64.b64decode(binary)
    old_avatar = current_user.avatar
    avatar_name = avatar.change_avatar(binary, old_avatar)
    current_user.avatar = avatar_name
    thumbnail_image = "thumbnail_{0}".format(avatar_name)
    src = '/'.join(['', current_app.config["AVATAR_IMAGE_PATH"], thumbnail_image])
    return message("success", {"src": src})


def change_cover(binary = None, *args, **kwargs):
    if not binary:
        return message("error", "", "数据有误")
    binary = base64.b64decode(binary)
    old_cover = current_user.cover
    cover_name = avatar.change_cover(binary, old_cover)
    current_user.cover = cover_name
    thumbnail_image = "thumbnail_{0}".format(cover_name)
    src = '/'.join(['', current_app.config["COVER_IMAGE_PATH"], thumbnail_image])
    return message("success", {"src": src})


AUTH_AJAX_METHODS = {
    "change_avatar": change_avatar,
    "change_cover": change_cover,
}


def auth_dispath_ajax(parameters, action):
    parameters = parameters.to_dict()
    method = AUTH_AJAX_METHODS.get(action)
    if not method:
        return message("error", "", "错误的操作类型")
    return method(**parameters)



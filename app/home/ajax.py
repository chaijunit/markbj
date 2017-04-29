#coding: utf-8

from flask import request,session, render_template, current_app, url_for
import random
from datetime import datetime
from app.common.ajax import *
from app.common.upload_file import *
from app.common.common import strdecode
from .models import *
from .import_html import *


def upload_tmpimg(*args, **kwargs):
    image = request.files.get("image")
    if not image or not validate_image(image.filename):
        return message("error", "", "数据有误")
    path, name = generate_tmpfile(image)
    value = {"url": path, "name":name}
    return message("success", value)


def change_tmpimg(filename = None, *args, **kwargs):
    image = request.files.get("image")
    if not image or not validate_image(image.filename):
        return message("error", "", "数据有误")
    if filename:
        remove_tmpfile(filename)
    path, name = generate_tmpfile(image)
    value = {"url": path, "name": name}
    return message("success", value)


def del_tmpimg(filename=None, *args, **kwargs):
    if not filename:
        return message('error', "", "数据有误")
    remove_tmpfile(filename)
    return message("success", "")


def import_html(html, url, only_main, download_image, image_path):
    """
    @param html: html内容
    @param url: 链接
    @param only_main: 值提取页面正文
    @param download_image: 要下载页面上的图片到本地
    @rapm image_path: 图片存放路径
    """
    html = get_url_html(html, url)
    if html is None:
        return message("warning", "", "地址无法访问")
    html = strdecode(html)
    html = html if not only_main else get_main_html(html)
    markdown = html2markdown(html, url, download_image, image_path)
    return message("success", markdown)


def import_article_html(html = None, url = None, only_main = None, 
        download_image= None, *args, **kwargs):
    only_main = 0 if only_main is None else int(only_main)
    download_image = 0 if download_image is None else int(download_image)
 
    if html is None and url is None:
        return message("warning", "", "内容不能为空")
    return  import_html(html = html, url = url, only_main = only_main,
            download_image= download_image, 
            image_path = current_app.config["ARTICLE_IMAGE_PATH"])


AUTH_AJAX_METHODS = {
    "upload_tmpimg": upload_tmpimg,
    "change_tmpimg": change_tmpimg,
    "del_tmpimg": del_tmpimg,
    "import_article_html": import_article_html, # 导入文章html

}

def auth_dispath_ajax(parameters, action):
    parameters = parameters.to_dict()
    method = AUTH_AJAX_METHODS.get(action)
    if not method:
        return message("error", "", "错误的操作类型")
    return method(**parameters)


def autosearch_topic(data, *args, **kwargs):
    topics = Topic.prefix_autosearch(data, 1, 
            current_app.config["AUTOSEARCH_TOPIC_PAGE"])
    value = {
        "topics": render_template("home/_search_topic_result.html", topics = topics.items),
        "page": render_template("home/_topic_pagination.html", endpoint="home.topic",
            pagination = topics, values = {"data": data})
    }
    return message("success", value)


AJAX_METHODS = {
    "autosearch_topic": autosearch_topic,
}


def dispath_ajax(parameters, action):
    parameters = parameters.to_dict()
    print 'parameters', parameters, action
    method = AJAX_METHODS.get(action)
    if not method:
        return message("error", "", "错误的操作类型")
    return method(**parameters)



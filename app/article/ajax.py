#coding: utf-8
from flask import current_app, request, session
from flask.ext.login import current_user
import hashlib
import simplejson as json
from app.common.upload_file import *
from app.common.common import merge_diff, description_diff
from app.common.ajax import *
from .models import *


def save_content(id, mdiff="", mtoken="", hdiff="", htoken=""):
    """ 保存文章内容 
    @param mdiff: markdown内容的diff信息
    @param mtoken: 验证markdown内容正确性
    @param hdiff: html内容的diff信息
    @param htoken: 验证html内容正确性
    """
    if not mdiff and not hdiff:
        return message("error", "", "数据有误")

    article = Article.query.filter_by(id=id).first()
    if not article or article.user_id != current_user.id:
        return message("error", "", "数据有误")

    mdiff = json.loads(mdiff)
    new_markdown = merge_diff(article.markdown, mdiff)
    mmd5 = hashlib.md5(new_markdown.encode("utf-8"))
    if mmd5.hexdigest() != mtoken:
        # 调用save_content_full 接口
        return message("warning", "mtoken error")

    hdiff = json.loads(hdiff)
    new_html = merge_diff(article.html, hdiff)
    hmd5 = hashlib.md5(new_html.encode('utf-8'))
    if hmd5.hexdigest() != htoken:
        # 调用save_content_full 接口
        return message("warning", "htoken error")

    article.save_content(new_markdown, new_html)
    return message("success", "保存成功")


def save_content_full(id, markdown = None, html=None):
    """ 保存目录内存 """
    if markdown is None or html is None:
        return message("error", "", "数据有误")

    article = Article.query.filter_by(id=id).first()
    if not article or article.user_id != current_user.id:
        return message("error", "", "数据有误")

    article.save_content(markdown, html)
    return message("success", "保存成功")


def upload_img(id, filename=None, name=None, *args, **kwargs):
    """ 上传图片 """
    article = Article.query.filter_by(id=id).first()
    if not article or article.user_id!=current_user.id:
        return message("error", "", "数据有误")

    image = ArticleImage.add(article.id, filename, name)
    value = {"id":image.id, "url":image.static_url(), "name": image.name}
    return message("success", value)


AUTH_AJAX_METHODS = {
    "save_content": save_content,
    "save_content_full": save_content_full,
    "upload_img": upload_img,
}


def auth_dispath_ajax(parameters, action):
    parameters = parameters.to_dict()
    method = AUTH_AJAX_METHODS.get(action)
    if not method:
        return message("error", "", "错误的操作类型")
    return method(**parameters)



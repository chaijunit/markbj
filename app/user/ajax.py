#coding: utf-8

from flask import current_app, request, render_template, url_for
from flask.ext.login import current_user
from datetime import datetime
from app.common.upload_file import *
from app.common.ajax import *
from app import db
import app
from .models import *


def remove_publish(id, source):
    """
    删除用户信息
    """
    if source != "article":
        return message("error", "", "数据有误")
    Article = app.article.models.Article
    article = Article.query.filter_by(id=id).filter_by(user_id=current_user.id).first()
    if not article:
        return message("error", "", "no article")
    article.delete()
    return message("success", "删除成功")


AUTH_AJAX_METHODS = {
    "remove_publish": remove_publish,
}


def auth_dispath_ajax(parameters, action):
    parameters = parameters.to_dict()
    method = AUTH_AJAX_METHODS.get(action)
    if not method:
        return message("error", "", "错误的操作类型")
    return method(**parameters)


def user_topic_url(source, t, user, tpage):
    if source != "article":
        return ""
    return url_for("user.article", topic=t.name, pathname=user.pathname, tpage=tpage)


def topic_page(tpage=1, uid=None,source=None):
    if not source or source != "article":
        return message("error", "", "数据有误")
    tpage = int(tpage)
    User = app.home.models.User
    user = User.query.filter_by(id=uid).first()
    if not user:
        return message("error", "", "用户不存在")
    Topic = app.home.models.Topic
    topics = Topic.get_user_article_topics(user.id, tpage)
    value = {}
    value["items"] = [{"name":t.name, "href":user_topic_url(source, t, user, tpage), "count": count} for t, count in topics.items]
    if topics.has_prev:
        value["prev"] = topics.prev_num
    if topics.has_next:
        value["next"] = topics.next_num
    return message("success", value)


AJAX_METHODS = {
    "topic_page":topic_page
}


def dispath_ajax(parameters, action):
    parameters = parameters.to_dict()
    method = AJAX_METHODS.get(action)
    if not method:
        return message("error", "", "错误的操作类型")
    return method(**parameters)



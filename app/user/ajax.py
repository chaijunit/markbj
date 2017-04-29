#coding: utf-8

from flask import current_app, request, render_template, url_for
from flask.ext.login import current_user
from datetime import datetime
from app.common.upload_file import *
from app.common.ajax import *
from app import db
import app
from .models import *


def add_follow(uid=None, *args, **kwargs):
    if not uid or current_user.id == int(uid):
        return message("error", "", "自己不能关注自己")
    User = app.home.models.User
    user = User.query.filter_by(id = uid).first()
    if not user:
        return message("error", "", "数据有误")
    follow_id = UserFollow.add_follow(current_user.id, user.id)
    if not follow_id:
        return message("error", "", "不能重复关注")
    return message("success", "关注成功")


def del_follow(uid=None, *args, **kwargs):
    if not uid or current_user.id == int(uid):
        return message('error', '', "数据有误")
    if not uid:
        return message("error", "", "数据有误")
    if not UserFollow.del_follow(current_user.id, uid):
        return message("error", "", "数据有误")
    return message("success", "取消关注成功")


def del_fans(uid = None, *args, **kwargs):
    if not uid or current_user.id == int(uid):
        return message("error", "", "数据有误")
    if not id:
        return message("error", "", "数据有误")
    if not UserFollow.del_follow(uid, current_user.id):
        return message("error", "", "数据有误")
    return message("success", "移除粉丝成功")


def remove_publish(id, source):
    """
    删除用户信息
    """
    if source=="book":
        Book = app.book.models.Book
        book = Book.query.filter_by(id=id).filter_by(user_id=current_user.id).first()
        if not book:
            return message("error", "", "no book")
        book.delete()
    elif source == "article":
        Article = app.article.models.Article
        article = Article.query.filter_by(id=id).filter_by(user_id=current_user.id).first()
        if not article:
            return message("error", "", "no article")
        article.delete()
    else:
        return message("error", "", "数据有误")
    return message("success", "删除成功")


AUTH_AJAX_METHODS = {
    "add_follow": add_follow,
    "del_follow": del_follow,
    "del_fans": del_fans,
    "remove_publish": remove_publish,
}


def auth_dispath_ajax(parameters, action):
    parameters = parameters.to_dict()
    print 'parameters', parameters
    method = AUTH_AJAX_METHODS.get(action)
    if not method:
        return message("error", "", "错误的操作类型")
    return method(**parameters)


def user_topic_url(source, t, user, tpage):
    if source=="publish":
        return url_for("user.index", topic=t.name, pathname=user.pathname, tpage=tpage)
    elif source=="book":
        return url_for("user.book", topic=t.name, pathname=user.pathname, tpage=tpage)
    elif source=="article":
        return url_for("user.article", topic=t.name, pathname=user.pathname, tpage=tpage)
    else:
        return ""

def topic_page(tpage=1, uid=None,source=None):
    if not source:
        return message("error", "", "数据有误")
    tpage = int(tpage)
    User = app.home.models.User
    user = User.query.filter_by(id=uid).first()
    if not user:
        return message("error", "", "用户不存在")
    Topic = app.home.models.Topic
    if source=="publish":
        topics = Topic.get_user_topics(user.id, tpage)
    elif source=="book":
        topics = Topic.get_user_book_topics(user.id, tpage)
    elif source=="article":
        topics = Topic.get_user_article_topics(user.id, tpage)
    else:
        return message("error", "", "数据有误")
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



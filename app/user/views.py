#coding:utf-8
from flask import jsonify, render_template, abort, redirect, request, url_for, flash, current_app
from . import user
from flask.ext.login import login_required,current_user
from app.home.models import User, Topic
from .models import *
from .ajax import auth_dispath_ajax, dispath_ajax


@user.route("/<id>")
def index(id):
    user = User.query.filter_by(id= id).first()
    if not user:
        return abort(404)
    topic = request.args.get("topic")
    page = request.args.get("page", 1, type=int)
    tpage = request.args.get("tpage", 1, type = int)
    articles = user.get_articles(page, topic)
    topics = Topic.get_user_article_topics(user.id, tpage)
    return render_template("user/index.html", user = user, articles = articles,
        topics = topics)


@user.route("/auth_ajax/<path:action>", methods=["GET", "POST"])
@login_required
def auth_ajax(action):
    return jsonify(auth_dispath_ajax(request.values, action))


@user.route("/ajax/<path:action>", methods=["GET", "POST"])
def ajax(action):
    return jsonify(dispath_ajax(request.values, action))



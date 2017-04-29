#coding:utf-8
from flask import jsonify, render_template, abort, redirect, request, url_for, flash
from . import article
import app
from flask.ext.login import login_required,current_user
from .forms import *
from app.home.models import Topic
from .models import *
from .ajax import auth_dispath_ajax


@article.route("/")
def index():
    page = request.args.get("page", 1, type = int)
    per_page = current_app.config["ARTICLE_PAGE"]
    articles = Article.get_articles(page, per_page)
    num = current_app.config["PREVIEW_TOPIC_NUM"]
    topics, total = Topic.get_article_topics(num)
    has_more = True if total > num else False
    return render_template("article/index.html", articles = articles, 
            topics = topics, has_more=has_more)


@article.route("/<pathname>")
def reader(pathname):
    article = Article.query.filter_by(pathname=pathname).first()
    if not article:
        return abort(404)
    if article.access == "private" and (not current_user.is_authenticated or \
            (current_user.is_authenticated and current_user.id != article.user.id)):
        return abort(404)
    return render_template("article/reader.html", article=article)


@article.route("/new", methods = ["GET","POST"])
@login_required
def new():
    form = ArticleForm()
    if form.validate_on_submit():
        topics = [topic.topic.data for topic in form.topics]
        article = Article.new(form.title.data, form.access.data,
            topics, current_user.id)
        return redirect(url_for("article.edit", pathname=article.pathname))
    return render_template("article/new.html", form=form)


@article.route("/setting/<pathname>", methods=["GET", "POST"])
@login_required
def setting(pathname):
    article = Article.query.filter(db.and_(Article.pathname == pathname, 
        Article.user_id == current_user.id)).first()
    if not article:
        return abort(404)
    form = ArticleForm()
    if form.validate_on_submit():
        topics = [topic.topic.data for topic in form.topics]
        article.setting(form.title.data, form.access.data,
            topics[:5])
        return redirect(url_for("user.index", id=current_user.id))
    return render_template("article/setting.html", article=article, 
            form = form)


@article.route("/edit/<pathname>")
@login_required
def edit(pathname):
    article = Article.query.filter_by(pathname=pathname).filter_by(
        user_id=current_user.id).first()
    if not article:
        return abort(404)
    return render_template("article/edit.html", article=article)


@article.route("/auth_ajax/<path:action>", methods=['GET', 'POST'])
@login_required
def auth_ajax(action):
    return jsonify(auth_dispath_ajax(request.values, action))



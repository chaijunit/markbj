#coding: utf-8
from flask import Response, jsonify, render_template, abort, session, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
import simplejson as json
import urllib
from . import home
from app import db
from .models import *
from .forms import *
from .ajax import auth_dispath_ajax, dispath_ajax
import random
import app
from app.common import avatar

@home.route("/")
def index():
    Article = app.article.models.Article
    newests = Article.newest_articles(20)
    return render_template("home/index.html", newests= newests)


@home.route("/topic")
def topic():
    _type = request.args.get("type", "all")
    name = request.args.get("topic")
    page = request.args.get("page", 1, type=int)
    topic = Topic.query.filter_by(name = name).first()
    if not topic:
        data = request.args.get("data", "")
        topics = Topic.prefix_autosearch(data, page,
                current_app.config["AUTOSEARCH_TOPIC_PAGE"])
        return render_template("home/topic.html", topics = topics)
    per_page = current_app.config["ARTICLE_PAGE"]
    articles = topic.get_articles(page, per_page)
    return render_template("home/topic-article.html", articles = articles, topic = topic)


@home.route("/login", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("user.index", id=current_user.id))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_user(form.email.data)
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember = form.remember_me.data)
            return redirect(url_for("user.index", id=user.id))
        flash("账号或密码错误")
    else:
        form.remember_me.data = True
    return render_template("home/login.html", form = form)


@home.route("/logout")
@login_required
def logout():
    logout_user()
    # 这里模仿facebook、twitter 都是返回首页
    return redirect(url_for("home.index"))


@home.route("/register", methods = ["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("user.index", id=current_user.id))
    form = RegisterForm()
    if form.validate_on_submit():
        if not User.check_email(form.email.data):
            form.email.errors.append("请输入正确的邮箱")
            return render_template("home/register.html", form = form)
        if User.query.filter_by(email = form.email.data).first():
            form.email.errors.append("该名称已经存在")
            return render_template("home/register.html", form = form)
        user = User.new(form.username.data, form.email.data, form.password.data)
        login_user(user)
        return redirect(url_for("user.index", id=user.id))
    return render_template("home/register.html", form=form)


@home.route("/password_forgot", methods=['GET', 'POST'])
def password_forgot():
    step = request.args.get('step')
    if step == "validate":
        email = session.get("validate_email")
        if not email:
            return redirect(url_for("home.password_forgot"))
        form = PasswordValidateForm()
        url = url_for("home.password_forgot", step="validate")
        if form.validate_on_submit():
            user = User.query.filter_by(email = email).first()
            if not user:
                return redirect(url_for("home.password_forgot"))
            if user.verification_code != form.verification_code.data:
                form.verification_code.errors.append("验证码错误!")
                return render_template("home/password_validate.html", form = form, url=url)
            if(datetime.now() - user.verification_code_timestamp).seconds>1800:
                form.verification_code.errors.append("验证码已经过期，请重新发送!")
                return render_template("home/password_validate.html", form = form, url=url)
            change_form = PasswordChangeForm()
            url = url_for("home.password_forgot", step="reset")
            session["verification_code"] = form.verification_code.data
            return render_template("home/password_change.html", form=change_form, url=url)
        return render_template("home/password_validate.html", form = form, url = url)
    elif step == 'reset':
        form = PasswordChangeForm()
        email = session.get("validate_email")
        if not email:
            return redirect(url_for("home.password_forgot"))
        user = User.query.filter_by(email=email).first()
        if not user:
            return redirect(url_for("home.password_forgot"))
        if form.validate_on_submit():
            if form.password.data != form.repeat_password.data:
                form.password.errors.append("两个密码不一样!")
                return render_template("home/password_change.html", form=form)
            user = User.query.filter_by(email=email).first()
            if not user:
                redirect(url_for("home.password_forgot"))
            user.password = User.generate_password_hash(form.password.data)
            session.pop("validate_email", None)
            if current_user.is_authenticated:
                # 退出
                logout_user()
            return redirect(url_for("home.login"))
        verification_code = session.get("verification_code")
        if verification_code:
            if user.verification_code==verification_code and (datetime.now()-user.verification_code_timestamp).seconds<1800:
                return render_template("home/password_change.html", form=form)
            session.pop("verification_code", None)
        return redirect(url_for("home.password_forgot"))
    form = PasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if not user:
            form.email.errors.append('您输入的账号不存在')
            return render_template("home/password_forgot.html", form=form)
        verification_code = random.randint(50, 999999)
        verification_code = "%0.6d"%(verification_code)
        user.verification_code = verification_code
        user.verification_code_timestamp = datetime.now()
        session['validate_email'] = form.email.data
        return redirect(url_for("home.password_forgot", step="validate"))
    return render_template("home/password_forgot.html", form = form)


@home.route("/search", methods=["GET"])
def search():
    Article = app.article.Article
    keyword = request.args.get("keyword", "")
    per_page = current_app.config["SEARCH_PAGE"]
    page = request.args.get("page", 1, type=int)
    articles = Article.search(keyword, page, per_page)
    return render_template("home/search.html", articles = articles)


@home.route("/auth_ajax/<path:action>", methods=['GET','POST'])
@login_required
def auth_ajax(action):
    return jsonify(auth_dispath_ajax(request.values, action))


@home.route("/ajax/<path:action>", methods=['GET','POST'])
def ajax(action):
    return jsonify(dispath_ajax(request.values, action))


@home.route("/robots.txt")
def robots():
    return Response(render_template("robots.txt"), mimetype ="text/plain", headers=[("Accept-Ranges", "bytes")])


@home.route("/sitemap.xml")
def sitemap():
    return Response(render_template("sitemap.xml"), mimetype ="text/xml", headers=[("Accept-Ranges", "bytes")])



#coding:utf-8
from flask import jsonify, render_template, abort, redirect, request, url_for, flash
from . import setting
import app
from flask.ext.login import login_required,current_user
from .ajax import auth_dispath_ajax
import re
from app import db
from .forms import *
import time


path_reg = re.compile(u'^[_a-zA-Z0-9]+$')


def validate_pathname(form):
    """
    验证个性化域名是否可用
    @param pathname: 个性化域名
    @param form: 设置基础信息的表单
    """
    pathname = form.pathname.data.lower()
    if len(pathname)<4:
        form.pathname.errors.append("长度不能小于4")
        return False
    
    if not path_reg.search(pathname):
        form.pathname.errors.append("含有非法字符")
        return False
    User = app.home.models.User
    if User.query.filter_by(pathname=pathname).first():
        form.pathname.errors.append("已经被使用")
        return False
    return True


@setting.route("/basic", methods=["GET", "POST"])
@login_required
def basic():
    form = BasicForm()
    if form.validate_on_submit():
        if not current_user.set_pathname and current_user.pathname!=form.pathname.data:
            # 如果用户未设置个性化域名
            if not validate_pathname(form):
                return render_template("setting/basic.html", form=form)
            current_user.pathname = form.pathname.data
            current_user.set_pathname = True
        flash("基础信息修改成功")
        current_user.username = form.username.data

        db.session.commit()
        return render_template("setting/basic.html", form=form)
    return render_template("setting/basic.html", form=form)


@setting.route("/password", methods=["GET", "POST"])
@login_required
def password():
    form = PasswordForm()
    if form.validate_on_submit():
        if not current_user.verify_password(form.old_password.data):
            form.old_password.errors.append("旧密码不正确")
            return render_template("setting/password.html", form=form)
        flash("密码修改成功")
        current_user.password = current_user.generate_password_hash(form.password.data)
        return render_template("setting/password.html", form=form)
    return render_template("setting/password.html", form=form)


@setting.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        flash("个人信息修改成功")
        current_user.setting_profile(form.profile.data,
            form.residence.data, form.profession.data[0])
        return render_template("setting/profile.html", form = form)
    return render_template("setting/profile.html", form=form)


@setting.route("/auth_ajax/<path:action>", methods=["GET", "POST"])
@login_required
def auth_ajax(action):
    return jsonify(auth_dispath_ajax(request.values, action))



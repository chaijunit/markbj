#coding:utf-8
from flask import Blueprint, request,render_template, jsonify
home = Blueprint("home", __name__)


@home.app_errorhandler(403)
def forbidden(e):
    if request.accept_mimetypes.accept_json  and \
        not request.accept_mimetypes.accept_html:
        response = jsonify({"status":"error", "value": "403", 'msg': 'forbidden'})
        response.status_code = 403 
        return response
    return render_template("home/403.html"), 403 


@home.app_errorhandler(404)
def forbidden(e):
    if request.accept_mimetypes.accept_json  and \
        not request.accept_mimetypes.accept_html:
        response = jsonify({"status":"error", "value": "404", 'msg': '页面找不到'})
        response.status_code = 404
        return response
    return render_template("home/404.html"), 404


@home.app_errorhandler(500)
def forbidden(e):
    if request.accept_mimetypes.accept_json  and \
        not request.accept_mimetypes.accept_html:
        response = jsonify({"status":"error", "value": "500", 'msg': 'forbidden'})
        response.status_code = 500
        return response
    return render_template("home/500.html"), 500


from .models import *
from . import views


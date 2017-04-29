#coding: utf-8
from flask import Blueprint
setting = Blueprint("setting", __name__)


from . import views


#coding: utf-8
from flask import Blueprint

article = Blueprint("article", __name__)

from .models import *
from . import views

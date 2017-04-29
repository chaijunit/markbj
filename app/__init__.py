#coding:utf-8
from flask import Flask, request, redirect

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from datetime import datetime

from config import config, Config

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db) 
    login_manager.init_app(app)


    # home 蓝图
    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    # user蓝图
    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix="/user")

    #文章
    from .article import article as article_blueprint
    app.register_blueprint(article_blueprint, url_prefix="/article")

    # setting 蓝图
    from .setting import setting as setting_blueprint
    app.register_blueprint(setting_blueprint, url_prefix="/setting")

    login_manager.login_view = "home.login"
    login_manager.login_message = "请先登录!!!"

    @app.template_filter("omit")
    def omit(data, length):
        if len(data) > length:
            return data[:length-3] + '...'
        return data

    @app.template_filter("friendly_time")
    def friendly_time(date):
        delta = datetime.now() - date
        if delta.days >= 365:
            return u'%d年前' % (delta.days / 365)
        elif delta.days >= 30:
            return u'%d个月前' % (delta.days / 30)
        elif delta.days > 0:
            return u'%d天前' % delta.days
        elif delta.seconds < 60:
            return u"%d秒前" % delta.seconds
        elif delta.seconds < 60 * 60:
            return u"%d分钟前" % (delta.seconds / 60)
        else:
            return u"%d小时前" % (delta.seconds / 60 / 60)

    return app 


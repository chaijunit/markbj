#coding: utf-8
import os
import app
import re
from datetime import datetime
from app import db, login_manager
from flask_login import current_user, UserMixin
from flask import current_app
from app.models import *
from sqlalchemy import func, union_all
from werkzeug.security import generate_password_hash, check_password_hash
from app.common import avatar

PREFIX = "home_"


class User(UserMixin, db.Model):
    """ 用户基础表 """
    __tablename__ = DB_PREFIX + "user"

    id = db.Column(db.Integer, primary_key = True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False, index=True, default="")
    email = db.Column(db.String(255), nullable=False, index=True)
    password =  db.Column(db.String(255), default="", nullable=False)

    cover = db.Column(db.String(255), default="")           # 封面图片文件名
    avatar = db.Column(db.String(255),  default="")           # 用户头像文件名
    verification_code = db.Column(db.String(255), default="")               # 验证码，用于修改密码时
    verification_code_timestamp = db.Column(db.DateTime, default = datetime.now)    # 验证码发送时间
    updatetime = db.Column(db.DateTime, default = datetime.now, nullable=False)      # 更新时间
    timestamp = db.Column(db.DateTime, default = datetime.now, nullable=False)       # 创建时间

    profile = db.relationship("UserProfile", backref="user", lazy="select", uselist=False)

    articles = db.relationship("Article", backref="user", lazy="dynamic")

    @staticmethod
    def new(username, email, password):
        user = User()
        user.username = username
        user.email = email
        user.password = User.generate_password_hash(password)
        user.avatar = avatar.init_avatar()
        db.session.add(user)
        db.session.commit()
        UserProfile = app.user.models.UserProfile
        profile = UserProfile()
        profile.user_id = user.id
        db.session.add(profile)
        return user

    def setting_profile(self, profile, residence, profession):
        self.profile.profile = profile
        self.profile.residence = residence
        self.profile.profession = profession

    @staticmethod
    def get_user(email):
        return User.query.filter_by(email = email).first()

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def check_email(email):
        if not re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", 
                email):
            return False
        return True

    @staticmethod
    def generate_password_hash(password):
        return generate_password_hash(password)

    def get_articles(self, page, topic=None):
        """ 获取用户发布的文章 """
        Article = app.article.models.Article
        per_page = current_app.config["USER_PAGE"]
        articles = db.session.query(Article).filter_by(user_id=self.id)
        if not current_user.is_authenticated or current_user.id!=self.id:
            articles = articles.filter_by(access="public")
        if topic:
            ArticleTopic = app.article.models.ArticleTopic
            Topic = app.home.models.Topic
            articles = articles.filter(Article.topics.any(ArticleTopic.topic.has(
                Topic.name==topic.lower())))
        articles = articles.order_by(Article.timestamp.desc())
        articles = paginate(articles, page, per_page=per_page, error_out=False)
        return articles

    def count_article(self):
        if not current_user.is_authenticated or current_user.id!=self.id:
            return self.articles.filter_by(access="public").count()
        return self.articles.count()

    def origin_cover(self):
        """ 原始大小封面 """
        image_path = "/".join(current_app.config["COVER_IMAGE_PATH"].split("/")[1:])
        return "/".join([image_path, self.cover])

    def thumbnail_cover(self):
        image_path = "/".join(current_app.config["COVER_IMAGE_PATH"].split("/")[1:])
        return "/".join([image_path, "thumbnail_{0}".format(self.cover)])

    def origin_avatar(self):
        """ 原始大小头像路径 """
        image_path = "/".join(current_app.config["AVATAR_IMAGE_PATH"].split("/")[1:])
        return "/".join([image_path, self.avatar])
    
    def thumbnail_avatar(self):
        """ 128*128大小头像 """
        image_path = "/".join(current_app.config["AVATAR_IMAGE_PATH"].split("/")[1:])
        return "/".join([image_path, "thumbnail_{0}".format(self.avatar)])

    def _50px_avatar(self):
        """ 50*50大小的头像 """
        image_path = "/".join(current_app.config["AVATAR_IMAGE_PATH"].split("/")[1:])
        filename =  "/".join([image_path, "50_50_{0}".format(self.avatar)])
        real_file = "/".join([current_app.root_path, filename])
        if not os.path.exists(real_file):
            return self.thumbnail_avatar()
        return filename
 
    def _20px_avatar(self):
        """ 20*20大小的头像 """
        image_path = "/".join(current_app.config["AVATAR_IMAGE_PATH"].split("/")[1:])
        return "/".join([image_path, "20_20_{0}".format(self.avatar)])


class Topic(db.Model):
    __tablename__ = DB_PREFIX + "topic"
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    name = db.Column(db.String(255), default = "", index = True, nullable = False)
    category_id = db.Column(db.Integer, default=0)  # 专题所属分类
    brief = db.deferred(db.Column(db.Text, default = "", nullable = False))
    avatar = db.Column(db.String(255), default = "", nullable = False)
    updatetime = db.Column(db.DateTime, default = datetime.now, nullable = False)
    timestamp = db.Column(db.DateTime, default = datetime.now, nullable = False)

    articles = db.relationship("ArticleTopic", backref="topic", lazy="dynamic")

    @staticmethod
    def prefix_autosearch(name, page, per_page):
        """ 标签名前缀查询 """
        Article = app.article.models.Article
        ArticleTopic = app.article.models.ArticleTopic
        topics = db.session.query(Topic).outerjoin(ArticleTopic, Article).filter(
                Topic.name.ilike(u"{0}%".format(name))).filter(Article.access=="public").group_by(
                Topic).order_by(func.count(ArticleTopic.topic_id).desc())
        return paginate(topics, page, per_page = per_page, error_out = False)

    @staticmethod
    def get_user_article_topics(user_id, page):
        per_page = current_app.config["USER_TOPIC_PAGE"]
        ArticleTopic = app.article.models.ArticleTopic
        Article = app.article.models.Article
        topics = db.session.query(Topic,
            func.count(ArticleTopic.topic_id).label("count"))\
            .outerjoin(ArticleTopic, Article).group_by(Topic)
        if not current_user.is_authenticated or current_user.id!=user_id:
            topics = topics.filter(db.and_(Article.user_id==user_id, 
                Article.access=="public"))
        else:
            topics = topics.filter(Article.user_id==user_id)
        topics = topics.order_by(func.count(ArticleTopic.topic_id).desc())
        topics = paginate(topics, page, per_page=per_page, error_out=False)
        return topics

    @staticmethod
    def get_article_topics(num):
        """ 所有文章的专题列表 
        @param num: 返回专题个数
        """
        ArticleTopic = app.article.models.ArticleTopic
        Article = app.article.models.Article
        topics = db.session.query(Topic)
        topics = topics.outerjoin(ArticleTopic).filter(
                ArticleTopic.article.has(Article.access=="public")
                ).group_by(Topic).order_by(
                func.count(ArticleTopic.topic_id).desc())
        return topics.limit(num).all(), topics.count()

    def get_articles(self, page, per_page):
        Article = app.article.models.Article
        ArticleTopic = app.article.models.ArticleTopic
        articles = db.session.query(Article).filter_by(access="public").outerjoin(
                ArticleTopic).filter(ArticleTopic.topic_id == self.id)
        return paginate(articles, page, per_page = per_page, error_out = False)

    def count_article(self):
        Article = app.article.models.Article
        return self.articles.outerjoin(Article).filter(Article.access=="public").count()


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


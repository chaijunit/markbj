#coding: utf-8
import os
import uuid
from datetime import datetime
from flask import current_app
from app import db
from app.models import * 
from app.home.models import User, Topic
from app.common.upload_file import *
from app.common.common import generate_code 
from bs4 import BeautifulSoup

PREFIX = "article_"

class Article(db.Model):
    __tablename__ = DB_PREFIX + PREFIX +"article"
    
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.__tablename__ + ".id", 
        ondelete="CASCADE", onupdate="CASCADE"), nullable = False)
    title = db.Column(db.String(255), default="", nullable=False)
    url = db.Column(db.String(255), default="", nullable = False)
    access = db.Column(db.String(255), default="public", nullable=False)    # 访问权限 public=> 公开 private=>私人

    markdown = db.deferred(db.Column(db.Text, default="", nullable=False))
    html = db.deferred(db.Column(db.Text, default = "", nullable=False))

    updatetime = db.Column(db.DateTime, default=datetime.now, nullable=False)
    timestamp = db.Column(db.DateTime, default = datetime.now, nullable=False)

    abstract = db.deferred(db.Column(db.Text, default = "", nullable=False))
    abstract_timestamp = db.Column(db.DateTime, default = datetime.now, nullable=False)
    cover = db.Column(db.String(255), default = "")
    cover_timestamp = db.Column(db.DateTime, default = datetime.now)
    pathname = db.Column(db.String(255), default=uuid.uuid1().hex, nullable=False)        # 文章的url路径名

    images = db.relationship("ArticleImage", backref="article", lazy="select", passive_deletes=True)

    topics = db.relationship("ArticleTopic", backref="article", lazy="select", passive_deletes=True)

    @staticmethod
    def new(title, access, topics, user_id):
        """ 新建文章 """
        article = Article()
        article.title = title
        article.access = access
        article.user_id = user_id
        db.session.add(article)
        db.session.commit()

        article.pathname = article.create_pathname()
        # 保存文章标签
        article.update_topics(topics[:5])

        return article
    
    @staticmethod
    def search(keyword, page, per_page):
        query = u"%{0}%".format(keyword)
        articles = Article.query.filter(db.and_(Article.access=="public",
            Article.title.ilike(query))).order_by(Article.updatetime.desc())
        return articles.paginate(page, per_page = per_page, error_out = False)

    @staticmethod
    def get_articles(page, per_page):
        """
        @param page: 当前页
        @param per_page: 每页个数
        """
        articles = Article.query.filter_by(access="public")
        return articles.paginate(page, per_page=per_page, error_out=False)

    @staticmethod
    def newest_articles(num):
        return Article.query.filter_by(access="public").order_by(
            Article.timestamp.desc()).limit(num).all()

    def create_pathname(self):
        """ 创建文章路径名 """
        code = generate_code(4)
        return "".join([code, str(self.id)])

    def setting(self, title, access, topics):
        """ 文章设置 """
        self.title = title
        self.access = access
        self.update_topics(topics)

    def get_cover(self):
        """ 取文章内容第一个图片作为文章的封面 """
        if self.updatetime > self.cover_timestamp:
            soup = BeautifulSoup(self.html, "lxml")
            img = soup.find("img")
            if img is not None:
                self.cover = img['src']
            else:
                self.cover = ""
            self.cover_timestamp = self.updatetime
        return self.cover

    def update_topics(self, topics):
        """ 更新文章标签 """
        new_topics = set([topic.strip().lower() for topic in topics])
        old_topics = set([topic.topic.name for topic in self.topics])

        delete_topics = old_topics - new_topics
        add_topics = new_topics - old_topics
        for name in delete_topics:
            self.delete_topic(name)
        for name in add_topics:
            self.add_topic(name)

    def add_topic(self, name):
        """ 添加标签 """
        if not name:
            return False
        topic = Topic.query.filter_by(name=name).first()
        if not topic:
            topic = Topic()
            topic.name = name
            db.session.add(topic)
            db.session.commit()
        for t in self.topics:
            if t.topic.name== name.lower():
                return False
        article_topic = ArticleTopic()
        article_topic.article_id = self.id
        article_topic.topic_id = topic.id
        db.session.add(article_topic)
        return True

    def delete_topic(self, name):
        """ 删除标签 """
        topic = Topic.query.filter_by(name=name).first()
        if not topic:
            return False
        ArticleTopic.query.filter_by(topic_id=topic.id).delete()
        return True

    def get_abstract(self):
        if not self.html:
            return ""
        if self.updatetime > self.abstract_timestamp:
            soup = BeautifulSoup(self.html, "lxml")
            self.abstract =  soup.get_text()[0:400]
            self.abstract_timestamp = self.updatetime
        return self.abstract

    def save_content(self, markdown, html):
        """ 保存文章内容 """
        self.markdown = markdown
        self.html = html
        self.updatetime = datetime.now()
 
    def delete(self):
        """ 删除文章 """
        # 删除文章图片
        for image in self.images:
            image.delete()
        # 删除标签
        for topic in self.topics:
            topic.delete()
        # 删除文章自己
        db.session.delete(self)


class ArticleImage(db.Model):
    __tablename__ = DB_PREFIX+PREFIX+"image"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255), default="", nullable=False)        # 图片名称(作为img标签的alt属性值)
    filename = db.Column(db.String(255), default="", nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey(Article.__tablename__+".id",
        ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    timestamp = db.Column(db.DateTime, default = datetime.now, nullable=False)

    def static_url(self):
        hostname = current_app.config["UPLOADIMG_HOST"]
        path = current_app.config["ARTICLE_IMAGE_PATH"]
        return '/'.join([hostname, path, self.filename])

    @staticmethod
    def add(article_id, filename, name):
        image = ArticleImage()
        image.name = name
        image.filename = filename
        image.article_id = article_id
        db.session.add(image)
        db.session.commit()
        # 将图片从tmp目录移到article images目录下
        dest_path = current_app.config["ARTICLE_IMAGE_PATH"]
        enable_tmpfile(dest_path, filename)
        return image

    def delete(self):
        path = current_app.config["ARTICLE_IMAGE_PATH"]
        remove_file(path, self.filename)
        db.session.delete(self)


class ArticleTopic(db.Model):
    __tablename__ = DB_PREFIX + PREFIX + "topic"
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    article_id = db.Column(db.Integer, db.ForeignKey(Article.__tablename__+".id",
        ondelete = "CASCADE", onupdate = "CASCADE"), nullable = False)
    topic_id = db.Column(db.Integer, db.ForeignKey(Topic.__tablename__ + ".id",
        ondelete = "CASCADE", onupdate = "CASCADE"), nullable = False)
    
    def delete(self):
        db.session.delete(self)



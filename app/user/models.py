#coding: utf-8
from datetime import datetime
from app import db
import app
from sqlalchemy import func, union_all, select , desc
from app.models import * 
from app.home.models import User
from app.common import data_config

PREFIX = "user_"


class UserProfile(db.Model):
    __tablename__ = DB_PREFIX+PREFIX+"profile"
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.__tablename__+".id",
        ondelete = "CASCADE", onupdate="CASCADE"), nullable=False)
    sex = db.Column(db.Integer, default = 1, nullable=False)        # 性别: 男==>1 女==>2
    profile = db.Column(db.Text, default="", nullable=False)
    residence = db.Column(db.String(255), default="", nullable=False)
    profession = db.Column(db.String(255), default="other", nullable=False)
    college = db.Column(db.String(255), default="", nullable=False)
    major = db.Column(db.String(255), default="", nullable=False)
    education = db.Column(db.String(255), default="", nullable=False)

    def profession2str(self):
        return data_config.profession_dict.get(self.profession, "其他")


class UserPublish(db.Model):
    '''
    用户发布表
    '''
    __tablename__ = DB_PREFIX+PREFIX+"publish"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.__tablename__+".id",
        ondelete = "CASCADE", onupdate="CASCADE"), nullable=False)
    publish_id = db.Column(db.Integer, default=0, nullable=False)
    source = db.Column(db.String(255), default="", nullable=False)
    timestamp = db.Column(db.DateTime, default = datetime.now, nullable=False)

    @staticmethod
    def search_all(keyword, page, per_page):
        Article = app.article.models.Article
        Book = app.book.models.Book
        query = u"%{0}%".format(keyword)
        publishs = db.session.query(UserPublish, Article, Book).outerjoin(Article, (
            db.and_(UserPublish.source=="article", UserPublish.publish_id==Article.id))).\
            outerjoin(Book, (db.and_(UserPublish.source=="book", 
                UserPublish.publish_id == Book.id))).filter(
                    db.or_(Article.access=="public", Book.access=="public")).filter(db.or_(
                    Article.title.ilike(query), Book.name.ilike(query))).order_by(
                    UserPublish.timestamp.desc())
        return paginate(publishs, page, per_page = per_page, error_out = False)

    @staticmethod
    def newest_publishs(num):
        Article = app.article.models.Article
        Book = app.book.models.Book
        publishs = db.session.query(UserPublish, Article, Book).outerjoin(Article, (
            db.and_(UserPublish.source=="article", UserPublish.publish_id==Article.id))).\
            outerjoin(Book, (db.and_(UserPublish.source=="book", 
                UserPublish.publish_id == Book.id))).filter(
                    db.or_(
                        db.and_(Article.access=="public", Article.is_necessary==0),
                        db.and_(Book.access=="public", Book.is_necessary==0)
                    )).group_by(UserPublish.id).order_by(
                    UserPublish.timestamp.desc()).limit(num).all()
        return publishs
 
    def source2publish(self):
        publish_source = {
            "book": app.book.models.Book,
            "article": app.article.models.Article,
        }
        return publish_source.get(self.source)





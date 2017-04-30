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





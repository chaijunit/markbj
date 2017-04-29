#coding: utf-8
from flask.ext.wtf import Form
from wtforms import StringField,RadioField, SubmitField
from wtforms import TextAreaField, FieldList, FormField
from wtforms.validators import DataRequired, Length


class _TopicForm(Form):
    topic = StringField("名称")


class ArticleForm(Form):
    title = StringField("标题", validators=[DataRequired("标题不能为空"), 
        Length(1,125, "长度不能超过125个字符")])
    topics = FieldList(FormField(_TopicForm))
    access = RadioField("访问权限", choices=[("public","公开"),("private","私人")])



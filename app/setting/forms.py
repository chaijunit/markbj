#coding: utf-8
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import RadioField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp
from app.common import data_config



class BasicForm(Form):
    username = StringField("用户名",  validators=[DataRequired("名称不能为空"),
        Regexp(u'^[_a-zA-Z0-9\u4e00-\u9fa5]+$', message="用户名含有非法字符"), 
        Length(2, 10, "名称长度应在2到10个字符之间")])
 
    pathname = StringField("个性域名")
    submit = SubmitField("保存更改")


class ProfileForm(Form):
    profile = TextAreaField("个性说明", validators=[Length(0, 120, "个性说明字数太长，最大不超过120个字符")])
    residence = StringField("现居住地", validators=[Length(0, 20, "地区字数不超过20")])
    profession = SelectMultipleField("行业", choices = data_config.profession_conf)


class PasswordForm(Form):
    old_password = StringField("旧密码", validators=[DataRequired("旧密码不能为空")])
    password = StringField("密码", validators = [DataRequired("密码不能为空"), Length(6,128, "密码长度应该在6到128字符之间")])
    repeat_password = StringField("确认密码", validators = [DataRequired("确认密码不能为空"), 
            EqualTo('password', '重复密码与密码不一致')])
    submit = SubmitField("保存更改")



#coding: utf-8
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length,Regexp


class LoginForm(Form):
    email = StringField("邮箱", validators=[DataRequired("邮箱不能为空")])
    password = PasswordField("密码", validators=[DataRequired("密码不能为空")])
    remember_me = BooleanField("记住我")
    submit = SubmitField("登录")


class RegisterForm(Form):
    username = StringField("用户名",  validators=[DataRequired("用户名不能为空"),
        Regexp(u'^[_a-zA-Z0-9\u4e00-\u9fa5]+$', message="用户名含有非法字符"), 
        Length(2, 10, "名称长度应在2到10个字符之间")])
    email = StringField("邮箱", validators=[DataRequired("邮箱不能为空")])
    password = PasswordField("密码", validators=[DataRequired("密码不能为空"), 
        Length(6, 128, "密码长度应该在6到128个字符之间")])
    submit = SubmitField("登录")


class SearchForm(Form):
    keyword = StringField("搜索关键字")
    submit = SubmitField("搜索")


class PasswordForm(Form):
    """
    忘记密码的账号
    """
    email = StringField("邮箱", validators = [DataRequired("邮箱不能为空")])
    submit = SubmitField("确定")


class PasswordValidateForm(Form):
    """
    重置密码的验证码
    """
    verification_code = StringField("验证码", validators = [DataRequired("验证码不能为空")])
    submit = SubmitField("确定")


class PasswordChangeForm(Form):
    """
    修改新密码
    """
    password = StringField("密码", validators = [DataRequired("密码不能为空"), Length(6,128, "密码长度应该在6到128字符之间")])
    repeat_password = StringField("确认密码", validators = [DataRequired("确认密码不能为空")])
    submit = SubmitField("确定")




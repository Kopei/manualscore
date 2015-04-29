# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'保持登入状态')
    submit = SubmitField(u'登入')


class RegistrationForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                           Email()])
    username = StringField(u'用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = PasswordField(u'密码', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField(u'确定密码', validators=[Required()])
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class ChangePasswordForm(Form):
    old_password = PasswordField(u'原密码', validators=[Required()])
    password = PasswordField(u'新密码', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'更新密码')


class PasswordResetRequestForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField(u'提交')


class PasswordResetForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField(u'密码', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'重置密码')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')


class ChangeEmailForm(Form):
    email = StringField('New Email', validators=[Required(), Length(1, 64),
                                                 Email()])
    password = PasswordField(u'密码', validators=[Required()])
    submit = SubmitField(u'更新邮箱')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

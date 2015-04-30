# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask.ext.pagedown.fields import PageDownField
from ..models import Role, User


class NameForm(Form):
    name = StringField(u'您的姓名?', validators=[Required()])
    submit = SubmitField(u'提交')


class EditProfileForm(Form):
    name = StringField(u'实名', validators=[Length(0, 64)])
    location = StringField(u'地区', validators=[Length(0, 64)])
    about_me = TextAreaField(u'关于我')

    submit = SubmitField(u'提交')


class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField(u'用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          u'用户名只能包含数字，字母，不能以数字和下划线开头！ ' )])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class PostForm(Form):
    title = StringField(u'标题', validators=[Required(), Length(1, 128)])
    body = TextAreaField(u"发表对一份手册的看法吧！", validators=[Required()])
    upload = FileField(u'您的手册')   #, #validators=[ FileAllowed(['pdf'], u'只支持pdf格式')])
    submit = SubmitField(u'发表')

#class Upload(Form):


class CommentForm(Form):
    body = StringField(u'评论', validators=[Required()])
    submit = SubmitField(u'提交')

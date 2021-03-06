# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
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
    degree = StringField(u'学历', validators=[Length(0, 31)])
    occupation = StringField(u"所属行业", validators=[Length(0,64)])
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
            raise ValidationError(u'邮箱已经被使用！请激活邮箱或换个邮箱。')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已经被使用。')


class PostForm(Form):

    title = StringField(u'标题', validators=[Required(), Length(1, 128)])
    body = PageDownField(u"发表对一份手册的看法吧！", validators=[Required()])
    tags = StringField(u'标签', validators=[Required(), Length(1, 128)])
    submit = SubmitField(u'发表')


class UploadForm(Form):
    upload = FileField(u'请先上传一份手册', validators=[FileRequired(u'请上传一份手册'), FileAllowed(['pdf'], u'只支持pdf格式')])
    submit = SubmitField(u'上传')

class CommentForm(Form):
    body = TextAreaField(u'评论', validators=[Required()])
    #submit = SubmitField(u'提交')


class SearchForm(Form):
    search = StringField('', validators=[Required()])
    submit = SubmitField(u'搜索')



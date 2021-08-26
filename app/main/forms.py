
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField,SelectMultipleField,widgets
from wtforms.fields.core import BooleanField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Email, Length, Regexp, ValidationError
from wtforms.widgets.core import TextArea
from ..model import Role,User


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class ShopForm(FlaskForm):
    name = StringField('商品名稱', validators=[DataRequired()])
    shop = MultiCheckboxField(u'商城', choices=[ ('1','蝦皮'),('2','PChome'),('3','露天')],default=['1','2','3'])
    minprice = StringField('最低價格', validators=[DataRequired()],default=0)
    maxprice = StringField('最高價格', validators=[DataRequired()],default=10000000000)
    submit = SubmitField('查詢')

class IndexForm(FlaskForm):
    name = StringField('使用者', validators=[DataRequired()])
    submit = SubmitField('查詢')

class EditProfileAdminForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Length(1,64),Email()])
    username=StringField('Username',validators=[DataRequired(),Length(1,64),
    Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters,numbers,dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role =SelectField('Role',coerce=int)
    name=StringField('Real name',validators=[Length(0,64)])
    location=StringField('Location',validators=[Length(0,64)])
    about_me=TextAreaField('About me')
    submit=SubmitField('Submit')

    def __init__(self, user,*args,**kwargs):
        super(EditProfileAdminForm,self).__init__(*args, **kwargs)
        self.role.choices=[(role.id,role.name) for role in Role.query.order_by(Role.name).all()]
        self.user=user

    def validate_email(self,field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')
    
    def validate_username(self,field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')

class EditProfileForm(FlaskForm):
    name=StringField('Real name',validators=[Length(0,64)])
    location=StringField('Location',validators=[Length(0,64)])
    about_me=TextAreaField('About me')
    submit=SubmitField('Submit')
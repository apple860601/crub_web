from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField,SelectMultipleField,widgets
from wtforms.fields.core import BooleanField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Email, Length, Regexp, ValidationError
from wtforms.widgets.core import TextArea
from ..model import Role,User
from flask_pagedown.fields import PageDownField

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class ShopForm(FlaskForm):
    name = StringField('商品名稱', validators=[DataRequired()])
    shop = MultiCheckboxField(u'商城', choices=[ ('1','蝦皮'),('2','PChome'),('3','露天')],default=['1','2','3'])
    minprice = StringField('最低價格', validators=[DataRequired()],default=0)
    maxprice = StringField('最高價格', validators=[DataRequired()],default=10000000000)
    submit = SubmitField('查詢')

class TraceForm(FlaskForm):
    product = StringField()
    trace = SubmitField('追蹤商品',id="trace", validators=[DataRequired()])
    cancel_submit = SubmitField('取消追蹤',id="cancel_trace", validators=[DataRequired()])
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)



from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

class EditForm(Form):
    nickname = TextAreaField('nickname', validators=[DataRequired()])
    fave_foods = TextAreaField('fave_foods', validators=[Length(min=0, max=140)])

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, PasswordField,BooleanField, FloatField
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo, NumberRange

#Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired(),EqualTo('password_hash2', message='Password Must Match')])
    password_hash2 = PasswordField('Confrim Password', validators=[DataRequired()])
    submit = SubmitField("Submit")


#Create a Form Class
class passwordForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password_hash = PasswordField('What is your Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Submit")


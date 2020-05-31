from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, FieldList, FileField, Form, FormField, IntegerField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class SignUpForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    submit = SubmitField('Login')


class RecipeForm(FlaskForm):
    prep_time = IntegerField('Prep time')
    cook_time = IntegerField('Cook time')
    date_added = DateField()
    servings = IntegerField('Servings')
    title = StringField('Recipe title', validators=[DataRequired()])
    description = TextAreaField(
        'Short description', validators=[DataRequired()])
    image = FileField('Upload image')
    quantity = StringField('Qty.', validators=[DataRequired()])
    measurement = StringField('Measure', validators=[DataRequired()])
    item = StringField('Item', validators=[DataRequired()])
    method = StringField('Method', validators=[DataRequired()])
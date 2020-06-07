from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, FieldList, FileField, Form, FormField, IntegerField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, number_range, ValidationError


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
                             validators=[DataRequired(), Length(min=6, max=12)])
    submit = SubmitField('Login')


class RecipeForm(FlaskForm):
    title = StringField('Recipe title', validators=[DataRequired()])
    description = TextAreaField(
        'Short description', validators=[DataRequired()])
    image = FileField('Upload image')
    quantity = StringField('Qty.', validators=[
                           DataRequired()])
    measurement = StringField('Measure', validators=[
                              DataRequired()])
    item = StringField('Item', validators=[DataRequired()])

    prep_time = IntegerField('Prep time (mins)', validators=[
                             number_range(min=0, message='Please enter a number (in minutes)')])
    cook_time = IntegerField('Cook time (mins)', validators=[
                             number_range(min=0, message='Please enter a number (in minutes)')])
    servings = IntegerField('Servings', validators=[
                            number_range(min=0, max=100)])
    method = StringField('Method', validators=[DataRequired()])
    date_added = DateField()
    

    

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.modelsWithNeo4j import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        print(username.data)
        user = User().get(username=username.data)
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User().get(email=email.data)
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            print("+++++++++++++++++++")
            print("before get")
            user = User().get(username=username.data)
            # changes
            print("after get")
            print(user, username.data, current_user.username)
            # end of changes
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User().get(email=email.data)
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class PortfolioForm(FlaskForm):
    name = StringField('Name of Portfolio', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AddStockToPortfolioForm(FlaskForm):
    name = StringField('Name of Stock', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SQLSearchForm(FlaskForm):
    payout_ratio_choices = [('Any','Any'), ('None','None'), ('Positive','Positive'), ('Low','Low'), ('High','High')]
    payout_ratio_field = SelectField('Payout Ratio', choices=payout_ratio_choices)

    operating_margin_choices = [('Any','Any'), ('Positive','Positive'), ('Negative','Negative'), ('High','High'),
                                ('Very Negative','Very Negative')]
    operating_margin_field = SelectField('Operating Margin', choices=operating_margin_choices)

    profit_margin_choices = [('Any','Any'), ('Positive','Positive'), ('Negative','Negative'), ('High','High')]
    profit_margin_field = SelectField('Profit Margin', choices=profit_margin_choices)

    submit = SubmitField('Search')

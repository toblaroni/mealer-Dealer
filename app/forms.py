from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError
from .models import User

# Form to register a new user
class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)],
                                       render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=6, max=20)],
                                       render_kw={"placeholder": "Password"})
    submit   = SubmitField("Register")

    def validate_username(self, username):
        existingUsername = User.query.filter_by(username=username.data).first()
        if existingUsername:
            raise ValidationError("That username already exists. Please choose a different one.")

# Form to login for existing users
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)],
                                       render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)],
                                       render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

# form to create a new meal deal
class mealDealForm(FlaskForm):
    main    = StringField("Main", validators=[InputRequired(), Length(min=0, max=40)])
    snack   = StringField("Snack", validators=[InputRequired(), Length(min=0, max=40)])
    drink   = StringField("Drink", validators=[InputRequired(), Length(min=0, max=40)])
    name    = StringField("Name your meal deal", validators=[InputRequired(), Length(min=0, max=50)])
    description = TextAreaField("Description", validators=[InputRequired(), Length(min=0, max=150)])
    submit  = SubmitField("Submit")

class changePasswordForm(FlaskForm):
    oldPassword = PasswordField(validators=[InputRequired(), Length(min=4, max=20)],
                                       render_kw={"placeholder": "Password"})
    newPassword = PasswordField(validators=[InputRequired(), Length(min=4, max=20)],
                                       render_kw={"placeholder": "Password"})
    submit  = SubmitField("Submit")

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField , IntegerField , SelectField
from wtforms.validators import InputRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


class ChangeForm(FlaskForm):
    oldpassword = PasswordField('old password', validators=[InputRequired(), Length(min=8, max=80)])
    newpassword = PasswordField('New password', validators=[InputRequired(), Length(min=8, max=80)])


class AddressForm(FlaskForm):
    address = StringField("address", validators=[InputRequired()])
    postal_code = StringField("postal code", validators=[InputRequired(), Length(min=6, max = 6)])
    country = SelectField("Select Country",validators=[InputRequired()],choices=[("Singapore","Singapore"),("Malaysia","Malaysia"),("Indonesia","Indonesia"),("Thailand","Thailand")])


class ForgotForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])


class SQuestionForm(FlaskForm):
    question = SelectField("Choose Question", validators=[InputRequired()],
                          choices=[("What is your mother's maiden name?", "What is your mother's maiden name?"),
                                   ("What is your pet's name?", "What is your pet's name?"),
                                   ("What is your favorite animal?", "What is your favorite animal?")])
    answer = StringField(validators=[InputRequired(), Length(max=100)])


class QuestionForm(FlaskForm):
    answer = StringField(validators=[InputRequired(), Length(max=100)])

class ResetChangeForm(FlaskForm):
    newpassword = PasswordField('New password', validators=[InputRequired(), Length(min=8, max=80)])
    confirmpassword = PasswordField('Confirm password', validators=[InputRequired(), Length(min=8, max=80)])

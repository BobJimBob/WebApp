from flask_wtf import *
from wtforms import *
from wtforms.fields.html5 import *
from wtforms.validators import *
from flask_wtf.file import *



class FeedbackForm(Form):
 fullName = StringField('Full Name', [validators.Length(min=1,max=150), validators.DataRequired()])
 email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
 feedback = TextAreaField('message', [validators.DataRequired()])

class CheckoutForm(Form):
 email = EmailField('Email',[validators.DataRequired(), validators.Email()])
 phone = IntegerField('Phone number')
 fullName = StringField('Full name', [validators.DataRequired()])
 optin = BooleanField('Opt in to our mailing list')
 address = StringField('Address', [validators.DataRequired()])
 city = StringField('City', [validators.DataRequired()])
 apartment = StringField('Apartment', [validators.DataRequired()])
 postalcode = StringField('Postal Code', [validators.DataRequired()])

'''
Bryans shit
'''



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

'''
eugenes shit
'''
class CreateProductForm(Form):
    productName = StringField('Product Name ',[validators.Length(min=1, max=150), validators.DataRequired()])
    author = StringField('Author', [validators.Length(min=1, max=150), validators.DataRequired()])
    publisher = StringField('Publisher', [validators.Length(min=1, max=150), validators.DataRequired()])
    genre = RadioField('Genre', choices=[('Children', 'Children'), ('Crime', 'Crime'), ('Fiction','Fiction'),('Manga','Manga')], default='Fiction')
    price =  StringField('Prices ',[validators.Length(min=1, max=150),validators.input_required()])
    remarks = TextAreaField('Product Description', [validators.Optional()])
    stocks = IntegerField("Stocks ",[validators.input_required()])

    image_1 = FileField("Image 1 ", validators=[FileAllowed(["jpg", "png", "jpgeg","webp"])])
    image_2 = FileField("Image 2 ", validators=[FileAllowed(["jpg", "png", "jpgeg","webp"])])
    image_3 = FileField("Image 3 ", validators=[FileAllowed(["jpg", "png", "jpgeg","webp"])])

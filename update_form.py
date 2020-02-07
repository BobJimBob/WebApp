from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators,IntegerField
from flask_wtf.file import FileRequired, FileAllowed, FileField



class UpdateProduct(Form):
    firstName = StringField('Product Name ',[validators.Length(min=1, max=150), validators.DataRequired()])
    lastName = StringField('Author', [validators.Length(min=1, max=150), validators.DataRequired()])
    publisher = StringField('Publisher', [validators.Length(min=1, max=150), validators.DataRequired()])
    membership = RadioField('Genre', choices=[('CH', 'Children'), ('CR', 'Crime'), ('F', 'Fiction'),('M','Manga')], default='F')
    price =  StringField('Prices ',[validators.Length(min=1, max=150)])
    remarks = TextAreaField('Procut Description', [validators.Optional()])
    stocks = IntegerField("Stocks ",[validators.input_required()])

    image_1 = FileField("Image 1 ", validators=[FileAllowed(["jpg", "png", "jpgeg"])])



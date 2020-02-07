from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators,IntegerField
from flask_wtf.file import FileRequired, FileAllowed, FileField



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



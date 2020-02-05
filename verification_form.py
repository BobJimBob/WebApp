from wtforms import Form, StringField, validators, DateField


class verification_form(Form):
    verifyDelivery = StringField('Verification Code', [validators.Length(min=1, max=150), validators.DataRequired()])

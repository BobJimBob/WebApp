from wtforms import Form, StringField,TextAreaField, validators, DateField

class remarksForms(Form):
    remarks = TextAreaField('Delivery Remarks: ', [validators.DataRequired()])

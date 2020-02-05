from wtforms import Form, StringField, SelectField, TextAreaField, validators, DateField


class alertForm(Form):
    deliveryStatus = SelectField('Delivery Status', [validators.Optional()],
                                 choices=[('D', 'Delivered'), ('DY', 'Delayed'), ('P', 'Processing')], default='DY')
    newDeliveryCompany = StringField('New Delivery Company', [validators.Length(min=1, max=150), validators.Optional()])
    newReceiveDate = DateField('New Receive Date (DD/MM/YYYY)', [validators.Optional()], format='%d/%m/%Y')
    remarks = TextAreaField('Remarks', [validators.DataRequired()])

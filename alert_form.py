from wtforms import Form, StringField, SelectField, TextAreaField, validators, DateField


class alertForm(Form):
    deliveryStatus = SelectField('Delivery Status', [validators.Optional()],
                                 choices=[('D', 'Delivered'), ('DY', 'Delayed'), ('P', 'Processing')], default='DY')
    newDeliveryTypes = SelectField('New Delivery Type', [validators.DataRequired()],
                                   choices=[('S', 'Normal Delivery'), ('A', 'Air Shipping')], default='S')
    newReceiveDate = DateField('New Receive Date (DD/MM/YYYY)', [validators.Optional()], format='%d/%m/%Y')
    remarks = TextAreaField('Remarks', [validators.DataRequired()])

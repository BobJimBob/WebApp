from wtforms import Form, StringField, SelectField, TextAreaField, validators, DateField


class createForm(Form):
    orderID = StringField('Order ID', [validators.Length(min=1, max=150), validators.DataRequired()])
    userID = StringField('User ID', [validators.Length(min=1, max=150), validators.DataRequired()])
    deliveryStatus = SelectField('Delivery Status', [validators.DataRequired()],
                                 choices=[('D', 'Delivered'), ('DY', 'Delayed'), ('P', 'Processing')], default='DY')
    newDeliveryTypes = SelectField('New Delivery Type', [validators.DataRequired()],
                                   choices=[('S', 'Normal Delivery'), ('A', 'Air Shipping')], default='S')
    newReceiveDate = DateField('New Receive Date (DD/MM/YYYY)', [validators.Optional()], format='%d/%m/%Y')
    remarks = TextAreaField('Remarks', [validators.DataRequired()])
    verificationCode = StringField('Verification', [validators.Length(min=1, max=150), validators.DataRequired()])

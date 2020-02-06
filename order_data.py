class Order:
    def __init__(self, orderID, date_sent, date_received, delivery_types, delivery_status, admin_remarks,
                 user_remarks, delivery_remarks, verification_code):
        self.__orderID = orderID
        self.__date_sent = date_sent
        self.__date_received = date_received
        self.__delivery_types = delivery_types
        self.__delivery_status = delivery_status
        self.__admin_remarks = admin_remarks
        self.__user_remarks = user_remarks
        self.__delivery_remarks = delivery_remarks
        self.__verification_code = verification_code

    def get_orderID(self):
        return self.__orderID

    def get_date_sent(self):
        return self.__date_sent

    def get_date_received(self):
        return self.__date_received

    def get_delivery_types(self):
        return self.__delivery_types

    def get_delivery_status(self):
        return self.__delivery_status

    def get_admin_remarks(self):
        return self.__admin_remarks

    def get_user_remarks(self):
        return self.__user_remarks

    def get_delivery_remarks(self):
        return self.__delivery_remarks

    def get_verification(self):
        return self.__verification_code

    def set_orderID(self, orderID):
        self.__orderID = orderID

    def set_date_sent(self, date_sent):
        self.__date_sent = date_sent

    def set_date_received(self, date_received):
        self.__date_received = date_received

    def set_delivery_types(self, delivery_types):
        self.__delivery_types = delivery_types

    def set_delivery_status(self, delivery_status):
        self.__delivery_status = delivery_status

    def set_admin_remarks(self, admin_remarks):
        self.__admin_remarks = admin_remarks

    def set_user_remarks(self, user_remarks):
        self.__user_remarks = user_remarks

    def set_delivery_remarks(self, delivery_remarks):
        self.__delivery_remarks = delivery_remarks

    def set_verification(self, verification_code):
        self.__verification_code = verification_code


#order1 = Order('100A', '25/1/2019', '26/1/2019', 'Fast Delivery', 'Delivered', '-')


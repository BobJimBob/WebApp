import shelve
import uuid
from datetime import date
class CartEntry:

    def __init__(self, itemID, image, name, price, quantity):

        self.__itemID = itemID
        self.__image = image
        self.__name = name
        self.__price = price
        self.__quantity = quantity
        self.__total = quantity*price

    def get_itemID(self):
        return self.__itemID
    def set_userID(self, itemID):
        self.__itemID = itemID

    def get_image(self):
        return self.__image
    def set_image(self, image):
        self.__image = image

    def get_name(self):
        return self.__name
    def set_name(self, name):
        self.__name = name

    def get_quantity(self):
        return self.__quantity
    def set_quantity(self, quantity):
        self.__quantity = quantity

    def get_price(self):
        return self.__price
    def set_price(self, price):
        self.__price = price

    def get_total(self):
        return self.__total
    def set_total(self, total):
        self.__total = total

class dbEntry:

    def __init__(self,itemID,image,name,price,invquantity):

        self.__itemID = itemID
        self.__image = image
        self.__name = name
        self.__price = price
        self.__invquantity = invquantity

    def get_itemID(self):
        return self.__itemID
    def set_userID(self, itemID):
        self.__itemID = itemID

    def get_image(self):
        return self.__image
    def set_image(self, image):
        self.__image = image

    def get_name(self):
        return self.__name
    def set_name(self, name):
        self.__name = name
    def get_price(self):
        return self.__price
    def set_price(self, price):
        self.__price = price

    def get_invquantity(self):
        return self.__invquantity
    def set_invquantity(self, invquantity):
        self.__invquantity = invquantity

class orderinfoC:
    def __init__(self, orderID, cartinfo, trackingnum):
        self.__orderID = orderID
        self.__cartinfo = cartinfo
        self.__trackingnum = trackingnum
        self.__status = "Processing"

    def get_orderID(self):
        return self.__orderID

    def set_orderID(self, orderID):
        self.__orderID = orderID

    def get_cartinfo(self):
        return self.__cartinfo

    def set_cartinfo(self, cartinfo):
        self.__cartinfo = cartinfo

    def get_trackingnum(self):
        return self.__trackingnum

    def set_trackingnum(self, trackingnum):
        self.__trackingnum = trackingnum

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status

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



class Product:
    countID = 0
    def __init__(self,productName,author,publisher,genre,price,stocks,remarks,image_1,image_2,image_3):
        Product.countID +=1
        productuuid = uuid.uuid4()
        self.__userID = str(productuuid)
        self.__productName = productName
        self.__author = author
        self.__publisher = publisher
        self. __genre = genre
        self.__price = price
        self.__stocks = stocks
        self.__remarks = remarks
        self.__image_1 = image_1
        self.__image_2 = image_2
        self.__image_3 = image_3




    def get_userID(self):
        return self.__userID

    def get_productName(self):
        return self.__productName

    def get_author(self):
        return self.__author


    def get_publisher(self):
        return self.__publisher

    def get_genre(self):
        return self.__genre

    def get_price(self):
        return self.__price


    def get_remarks(self):
        return self.__remarks


    def get_stocks(self):
        return self.__stocks


    def get_image_1(self, ):
        return self.__image_1

    def get_image_2(self,):
        return self .__image_2

    def get_image_3(self, ):
        return self.__image_3


    def set_userID(self,userID):
        self.__userID = userID

    def set_productName(self,productName):
        self.__productName = productName

    def set_author(self,author):
        self.__author = author

    def set_genre(self,genre):
         self.__genre = genre


    def set_publisher(self,publisher):
        self.__publisher = publisher

    def set_price(self,price):
        self.__price = price

    def set_remarks(self,remarks):
        self.__remarks = remarks

    def set_stocks(self,stocks):
        self.__stocks = stocks

    def set_image_1(self,image_1):
        self.__image_1 = image_1

    def set_image_2(self, image_2):
        self.__image_2 = image_2

    def set_image_3(self, image_3):
        self.__image_3 = image_3


inventory = shelve.open('inventory.db', 'c')

def create_new_dbItem( name, image, price,invquantity):
    id = str(uuid.uuid4())
    print (id)
    item = dbEntry(id,image,name,price,invquantity)
    item.name = name
    item.image = image
    item.price = price
    item.invquantity = invquantity
    inventory[id] = item

def update_dbItem(item):
    inventory[item.id] = item


def delete_dbItem(id):
    if id in inventory:
        del inventory[id]


def clear_inventory():
    klist = list(inventory.keys())
    for key in klist:
        del inventory[key]


def initdb():
    clear_inventory()
    create_new_dbItem('book 1', '/static/images/img1.jpg', 20, 50)
    create_new_dbItem('Book 2', '/static/images/img2.jpg', 30, 43)
    create_new_dbItem('Book 3', '/static/images/img3.jpg', 40, 60)
    create_new_dbItem('Book 4', '/static/images/img4.jpg', 50, 70)

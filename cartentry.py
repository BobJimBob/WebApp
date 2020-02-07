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
    create_new_dbItem( 'book 1', '/static/images/img1.jpg', 20, 50)
    create_new_dbItem( 'Book 2', '/static/images/img2.jpg', 30,43)
    create_new_dbItem( 'Book 3', '/static/images/img3.jpg', 40,60)
    create_new_dbItem('Book 4', '/static/images/img4.jpg', 50, 70)

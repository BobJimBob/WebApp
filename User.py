class User:
    countID = 0
    def __init__(self,productName,author,publisher,genre,price,stocks,remarks,image_1,image_2,image_3):
        User.countID +=1
        self.__userID = User.countID
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
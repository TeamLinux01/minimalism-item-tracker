from dataclasses import dataclass
import datetime

@dataclass
class Thing:
    """Physical objects or things a person can claim ownership of.
    Stores the name, how many, location, and if it is still in the home.
    Optionally stores the date (YYYY/MM/DD) it entered the home, how much it was purchased for, and its UPC."""

    def __init__(self, name, location, amount=1, inHome="", price="", upc=""):
        """Only name and location are required"""
        self.name = name            # object or thing name
        self.amount = amount        # amount of objects or things
        self.location = location    # location of object or thing
        self.dateInHome = inHome    # date brought into home, format YYYY, MM, DD
        self.price = price          # price of object or thing
        self.upc = upc              # Universal Product Code of object or thing 
        self.stillOwned = True      # If the object or thing is still owned

    @property
    def name(self):
        """Get name of the object or thing"""
        return self.__name

    @name.setter
    def name(self, name):
        """Set name of the object or thing"""
        self.__name = str(name)

    @property
    def amount(self):
        """Get amount of the objects or things"""
        return self.__amount

    @amount.setter
    def amount(self, amount):
        """Set an amount of the object or thing"""
        self.__amount = int(amount)

    @property
    def location(self):
        """Get the physical location of the object or thing"""
        return self.__location

    @location.setter
    def location(self, location):
        """Set the physical location of the object or thing"""
        self.__location = str(location)

    @property
    def dateInHome(self):
        """Get the date the object or thing entered the home"""
        return self.__dateInHome

    @dateInHome.setter
    def dateInHome(self, inHome):
        """Set the date for the object or thing entering the home
        Accepts dates in YYYY, MM, DD format, returns YYYY-MM-DD"""
        if len(str(inHome)) == 0:
            self.__dateInHome = ""
        else:
            _dt = datetime.datetime.strptime(inHome, '%Y, %m, %d')
            self.__dateInHome = datetime.date(_dt.year, _dt.month, _dt.day)

    @property
    def price(self):
        """Get the price of the object or thing"""
        return self.__price

    @price.setter
    def price(self, price):
        """Set the price of the object or thing"""
        self.__price = round(float(price), 2)

    @property
    def upc(self):
        """Get the Universal Product Code of the object or thing"""
        return self.__upc

    @upc.setter
    def upc(self, upc):
        """Set the Universal Product Code of the object or thing"""
        upc = str(upc)
        if (len(upc) == 12) or (len(upc) == 0):
            self.__upc = upc
        else:
            raise ValueError("UPC bar codes are 12 digits")

    @property
    def stillOwned(self):
        """Get if the object or thing is still owned"""
        return self.__stillOwned

    @stillOwned.setter
    def stillOwned(self, stillOwned):
        """Set if the object or thing is still owned"""
        self.__stillOwned = bool(stillOwned)

    def getStr(self):
        """Return a string of all the objects attributes
        Will not include defaults"""
        if self.__stillOwned == False:
            owned = "No"
        elif self.__stillOwned == True:
            owned = "Yes"
        
        _returnStr = str("Name: " + self.__name + "\n" + \
                   "Amount:" + str(self.__amount) + "\n" + \
                   "Location: " + self.__location + "\n" + \
                   "Owned: " + owned + "\n")

        if len(str(self.__dateInHome)) != 0:
            _returnStr += str("Date entered home: " + str(self.__dateInHome) + "\n")

        if len(str(self.__price)) != 0:
            _returnStr += str("Price: " + str(self.__price) + "\n")
        
        if len(str(self.__upc)) != 0:
            _returnStr += str("UPC: " + self.__upc + "\n")

        return _returnStr
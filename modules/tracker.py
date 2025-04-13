#!/bin/python3

from dataclasses import dataclass
import datetime

@dataclass
class Item:
    """Physical item a person can claim ownership of.
    Stores the name, how many of the item, location of item, and if it is still in the home.
    Optionally stores the date it entered the home (enter as "YYYY-MM-DD), how much it was purchased for, and its UPC."""

    def __init__(self, name, location, amount=1, inHome="", price="", upc=""):
        """Only name and location are required"""
        self.name = name            # item name
        self.amount = amount        # item amount
        self.location = location    # location of item
        self.dateInHome = inHome    # date item was brought into home, format is "YYYY, MM, DD"
        self.price = price          # price of item
        self.upc = upc              # Universal Product Code of item 
        self.stillOwned = True      # If the item is still owned

    def __str__(self):
        return self.getStr()
    
    @property
    def name(self):
        """Get name of the item"""
        return self.__name

    @name.setter
    def name(self, name):
        """Set name of the item"""
        self.__name = str(name)

    @property
    def amount(self):
        """Get amount of the item"""
        return self.__amount

    @amount.setter
    def amount(self, amount):
        """Set an amount of the item"""
        if amount == 0:
            self.__stillOwned = False
        self.__amount = int(amount)

    @property
    def location(self):
        """Get the physical location of the item"""
        return self.__location

    @location.setter
    def location(self, location):
        """Set the physical location of the item"""
        self.__location = str(location)

    @property
    def dateInHome(self):
        """Get the date the item entered the home"""
        return self.__dateInHome

    @dateInHome.setter
    def dateInHome(self, inHome):
        """Set the date for the item entering the home
        Accepts dates in YYYY, MM, DD format, returns date object YYYY-MM-DD"""
        if len(str(inHome)) == 0:
            self.__dateInHome = ""
        else:
            _dt = datetime.datetime.strptime(inHome, '%Y, %m, %d')
            self.__dateInHome = datetime.date(_dt.year, _dt.month, _dt.day)

    @property
    def price(self):
        """Get the price of the item"""
        return self.__price

    @price.setter
    def price(self, price):
        """Set the price of the item"""
        if len(str(price)) == 0:
            self.__price = ""
        else:
            self.__price = round(float(price), 2)

    @property
    def upc(self):
        """Get the Universal Product Code of the item"""
        return self.__upc

    @upc.setter
    def upc(self, upc):
        """Set the Universal Product Code of the item"""
        upc = str(upc)
        if (len(upc) == 12) or (len(upc) == 0):
            self.__upc = upc
        else:
            raise ValueError("UPC bar codes are 12 digits")

    @property
    def stillOwned(self):
        """Get if the item is still owned"""
        return self.__stillOwned

    @stillOwned.setter
    def stillOwned(self, stillOwned):
        """Set if the item is still owned"""
        if stillOwned == False: # If it is not owned any more, set the amount to none
            self.__amount = 0
        self.__stillOwned = bool(stillOwned)

    def getStr(self):
        """Return a string of all the item's attributes
        Will not include defaults"""
        if self.__stillOwned == False:
            owned = "No"
        elif self.__stillOwned == True:
            owned = "Yes"
        
        _returnStr = str("Name: " + self.__name + "\n" + \
                         "Location: " + self.__location + "\n" + \
                         "Item amount: " + str(self.__amount) + "\n" + \
                         "Item still owned: " + owned + "\n")

        if len(str(self.__dateInHome)) != 0:
            _returnStr += str("Date item entered home: " + str(self.__dateInHome) + "\n")

        if len(str(self.__price)) != 0:
            _returnStr += str("Price: " + str(self.__price) + "\n")
        
        if len(str(self.__upc)) != 0:
            _returnStr += str("UPC: " + self.__upc + "\n")

        return _returnStr
    
def main():
    """ Tests the Item class"""
    print("This tests the Item class")
    items = [Item("Chair", "Office"),
             Item("Desk", "Office"),
             Item("Table", "Dinning")]
    printItems(items)
    items[0].stillOwned = False
    items[1].amount = 0
    printItems(items)

def printItems(items):
    for item in items:
        print(item)

if __name__ == "__main__":
    main()
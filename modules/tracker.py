#!/bin/python3

from dataclasses import dataclass

@dataclass
class Item:
    """Physical item a person can claim ownership of.
    Stores the name and how many of the item.
    Optionally stores its location and price."""

    def __init__(self, name, location="", amount=1, price=""):
        self.name = name            # item name
        self.location = location    # item location
        self.amount = amount        # item amount
        self.price = price          # price of item

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

    def getStr(self):
        """Return a string of all the item's attributes
        Will not include defaults"""
        _returnStr = str("Name: " + self.__name + ", " + \
                         "Item amount: " + str(self.__amount))

        if len(str(self.__location)) != 0:
            _returnStr += str(", Location: " + str(self.__location))

        if len(str(self.__price)) != 0:
            _returnStr += str(", Price: $" + str(self.__price))

        return _returnStr
    
def main():
    """ Tests the Item classes"""

    print("This tests the Item class")
    items = [Item("Chair"),
             Item("Desk"),
             Item("Table")]
    printItems(items)
    items[1].amount = 0
    printItems(items)

    items.append(Item("Spoon", "cabinet", 3, 5))
    printItems(items)
    print()
    items[0].name = "Boat"
    printItems(items)

def printItems(items):
    for item in items:
        print(item)

if __name__ == "__main__":
    main()
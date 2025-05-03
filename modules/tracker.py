#!/bin/python3

from dataclasses import dataclass

@dataclass
class Item:
    '''Physical item a person can claim ownership of.
    Stores the name and how many of the item.
    Optionally stores its location and price.'''

    def __init__(self, name, amount=1, location="", price=""):
        self.name = name            # item name
        self.amount = amount        # item amount
        self.location = location    # item location
        self.price = price          # price of item

    def __str__(self):
        return self.getStr()
    
    def __iter__(self):
        '''Allows the Item object to be iterated, returns name, amount, location and price in that order'''
        _valuesList = [self.name, self.amount, self.location, self.price]
        for value in _valuesList:
            yield value
    
    @property
    def name(self):
        '''Get name of the item'''
        return self.__name

    @name.setter
    def name(self, name):
        '''Set name of the item'''
        self.__name = str(name)

    @property
    def amount(self):
        '''Get amount of the item'''
        return self.__amount

    @amount.setter
    def amount(self, amount):
        '''Set an amount of the item'''
        self.__amount = int(amount)

    @property
    def location(self):
        '''Get the physical location of the item'''
        return self.__location

    @location.setter
    def location(self, location):
        '''Set the physical location of the item'''
        self.__location = str(location)

    @property
    def price(self):
        '''Get the price of the item'''
        return self.__price

    @price.setter
    def price(self, price):
        '''Set the price of the item'''
        # If price is 0, store as an empty return empty string instead, otherwise return as a rounded float
        if len(str(price)) == 0:
            self.__price = ""
        else:
            self.__price = round(float(price), 2)

    def getStr(self):
        '''Return a string of all the item's attributes
        Will not include attributes with optional default values'''
        _returnStr = str("Name: " + self.__name + ", " + \
                         "Item amount: " + str(self.__amount))

        if len(str(self.__location)) != 0:
            _returnStr += str(", Location: " + str(self.__location))

        if len(str(self.__price)) != 0:
            _returnStr += str(", Price: $" + str(self.__price))

        return _returnStr # returns a string of "Name: {name}, Amount: {amount}" and then if there are values it takes on "Location: {location}" and "Price: {price}" as comma separated values
    
def main():
    '''Tests the Item classes'''

    print("This tests the Item class")
    # Make a list of three items
    items = [Item("Chair"),
             Item("Desk"),
             Item("Table")]
    printItems(items) # Prints the list of items
    items[1].amount = 6.33 # Rounds the number to 6
    printItems(items)

    items.append(Item("Spoon", 3, "cabinet", 5))
    printItems(items)
    print()
    items[0].name = "Boat" # Changes the Chair to a Boat
    printItems(items)

def printItems(items):
    '''Goes through each item in the items list, prints out the data for the item'''
    for item in items:
        print(item)

if __name__ == "__main__":
    main()
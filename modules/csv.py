import csv
from modules.tracker import Item

def SaveCSV(items):
    '''Saves "item_tracker.csv" file with a header in the first row and data in all other rows'''
    with open('item_tracker.csv', 'w') as csvfile:
        file = csv.writer(csvfile)
        file.writerow(["name","amount","location","price"])
        for item in items:
            file.writerow(item)

def LoadCSV():
    '''Opens "item_tracker.csv""" file and returns a list of each Item object for each row'''
    with open('item_tracker.csv') as csvfile:
        reader = csv.DictReader(csvfile)        # reads the file, looks for header row for dictionary names
        items = []                              # Prepares an empty list
        for row in reader:                      # Adds an Item object for each data row in the file to the list
            items.append(Item(name=row['name'], amount=row['amount'], location=row['location'], price=row['price']))
        return items                            # Returns the populated list

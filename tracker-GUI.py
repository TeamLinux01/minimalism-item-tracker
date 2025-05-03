#!/bin/python3

import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from modules.tracker import Item
import modules.database as db
import modules.csv as csv

class MainFrame(ttk.Frame):
    """The main window frame to draw the interface"""
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="2 2 2 2")
        self.parent = parent
        self.vcmd = (self.register(self.Validate),              # validation variable to check entry boxes for just numbers
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.textFrame = TextFrame(self)                        # Frame for the big textbox
        self.commandFrame = CommandFrame(self)                  # Frame where the add, edit and delete buttons live
        self.statsFrame = StatsFrame(self)                      # Frame that shows the total types, amounts and price

        # Initialize the temp storage variables for what will be put into the Item class objects
        self._itemName = ""
        self._itemLocation = ""
        self._itemAmount = 0
        self._itemPrice = 0

        self._items = [] # list of all the item objects

        db.connect()        # Open sqlite3 database file "db.sqlite3"
        db.check_database() # Check to see if there data in the "Item" table and if there isn't, it creates the "Item" table

        self.RefreshDisplayData() # Enter any data from initial load into the big textbox

        self.initComponents()

    def initComponents(self):
        """Initialize drawing of Main frame"""
        self.pack(fill=tk.BOTH, expand=True)    # Fill the frame's geometry for drawing

        # command buttons on top, big textbox in the middle, stats on the bottom
        self.commandFrame.grid(
            column=0, row=0
        )
        self.textFrame.grid(
            column=0, row=1
        )
        self.statsFrame.grid(
            column=0, row=2
        )

    def RefreshDisplayData(self):
        """Clears the big textbox, inserts the item data in each line"""
        self.textFrame.itemsText.configure(state='normal')      # Required to write data to the big textbox
        self.textFrame.itemsText.delete('1.0', 'end')           # Delete all text in the big textbox
        self.textFrame.itemsText.insert('end', 'Name:\t\t\t\t\t\t\t\tAmount:\t\t\tLocation:\t\t\t\t\t\t\t\tPrice:\n')   # Draw header
        for _item in self._items:                               # Add all items in the list to the big textbox, linebreak after each time
            self.textFrame.itemsText.insert('end', _item.name + '\t\t\t\t\t\t\t\t' + str(_item.amount) + '\t\t\t' + _item.location + '\t\t\t\t\t\t\t\t$' + str(_item.price) + '\n')

        self.textFrame.itemsText.configure(state='disabled')    # Make big textbox readonly again

        for entry in self.statsFrame._entries:                  # Required to write data to stats entry boxes
            entry['state'] = 'normal'
        
        _totalAmount = 0
        _totalPrice = 0
        for item in self._items:                    # Add up the price for all the items
            _totalAmount += item.amount
            if item.price == "":
                _price = 0
            else:
                _price = item.amount * item.price

            _totalPrice += _price
        
        self.statsFrame.entryTotalItems.set_text(len(self._items))  # Enter the amount of item entries into the stats entry box
        self.statsFrame.entryTotalAmount.set_text(_totalAmount)     # Enter the total amount of items into the stats entry box
        self.statsFrame.entryTotalPrice.set_text(_totalPrice)       # Enter the total price of items into the stats entry box

        for entry in self.statsFrame._entries:                      # Make stats entry boxes readonly again
            entry['state'] = 'readonly'

    def RefreshInputData(self, parent, index):              # Sync data from variables in frames to the entry boxes' text; "parent" is the frame calling the method
        parent._itemIndex = index+1                         # Add 1 to index to display correctly
        parent.comboboxIndex.set(parent._itemIndex)
        parent._itemName = parent._items[index].name
        parent.entryName.set_text(parent._itemName)
        parent._itemLocation = parent._items[index].location
        parent.entryLocation.set_text(parent._itemLocation)
        parent._itemAmount = parent._items[index].amount
        parent.entryAmount.set_text(parent._itemAmount)
        parent._itemPrice = parent._items[index].price
        parent.entryPrice.set_text(parent._itemPrice)

    def Validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        '''Validates if text is allowed in an entry box, used for the amount and price boxes to check, so only floats are added
           Empty string is also allowed'''
        if value_if_allowed:
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        elif value_if_allowed == "":
            return True
        else:
            return False
        
class CommandFrame(ttk.Frame):
    '''Frame that has the buttons that run commands'''
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, borderwidth=5, relief="groove", padding="5 5 5 5")
        self.parent = parent
        self.mainframe = parent # Easy way to access the MainFrame object's properties and methods
   
        self.initComponents()

    def initComponents(self):
        '''Initialize drawing of Command frame'''
        _gridArgs = {"padx":90, "pady":5}   # Set the extra space between the grid objects

        # Create and draw all the buttons
        self.buttonAddItem = displayButton(self, text="Add Item", command=self.AddItem).grid(
            column=0, row=0, **_gridArgs
        )
        self.buttonEditItem = displayButton(self, text="Edit Item", command=self.EditItem).grid(
            column=0, row=1, **_gridArgs
        )
        self.buttonDeleteItem = displayButton(self, text="Delete Item", command=self.DeleteItem).grid(
            column=0, row=2, **_gridArgs
        )
        self.buttonSaveData = displayButton(self, text="Save Data", command=self.SaveData).grid(
            column=1, row=0, **_gridArgs
        )
        self.buttonLoadData = displayButton(self, text="Load Data", command=self.LoadData).grid(
            column=1, row=1, **_gridArgs
        )
        self.buttonExportData = displayButton(self, text="Export CSV", command=self.ExportCSV).grid(
            column=2, row=0, **_gridArgs
        )
        self.buttonImportData = displayButton(self, text="Import CSV", command=self.ImportCSV).grid(
            column=2, row=1, **_gridArgs
        )
    
    def AddItem(self):
        '''Pops up an Add Item Window'''
        self.addWindow = AddWindow(self.mainframe, master=root).resizable(0, 0)         # Window is not resizable

    def EditItem(self):
        '''Pops up an Edit Item Window'''
        self.editWindow = EditWindow(self.mainframe, master=root).resizable(0, 0)       # Window is not resizable
    
    def DeleteItem(self):
        '''Pops up a Delete Item Window'''
        self.deleteWindow = DeleteWindow(self.mainframe, master=root).resizable(0, 0)   # Window is not resizable

    def SaveData(self):
        '''Saves the data to the db file'''
        if len(self.mainframe._items) == 0 and len(db.check_database()) != 0:                                   # Check if the items list is empty and the database is not empty
            if messagebox.askokcancel("Delete database?", "Would you like to delete the database?") == True:    # Warn user if about saving an empty list to a non-empty database
                db.clearDatabase()                  # Destroy the database
                for _item in self.mainframe._items: # Add a blank list to the database
                    db.add_item(_item)
        else:
            db.clearDatabase()                      # Destroy the database
            for _item in self.mainframe._items:     # Add all the items back to the database
                db.add_item(_item)  

    def LoadData(self):
        '''Loads the data from the db file'''
        self.databaseItems = db.load_data()         # Load the database items into a temporary object
        self.mainframe._items.clear()               # Clear the items list
        for item in self.databaseItems:             # Add to the items list all the database items from the temporary object
            self.mainframe._items.append(Item(name=item['name'], amount=item['amount'], location=item['location'], price=item['price']))
        self.mainframe.RefreshDisplayData()         # Refresh screen data

    def ExportCSV(self):
        '''Exports the data to the csv file'''
        csv.SaveCSV(self.mainframe._items)

    def ImportCSV(self):
        '''Imports the data from the csv file'''
        self.mainframe._items = csv.LoadCSV()   # Replace the items list with the csv items data
        self.mainframe.RefreshDisplayData()     # Refresh screen data

class TextFrame(ttk.Frame):
    '''Frame that has the big textbox to display data'''
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.mainframe = parent # Easy way to access the MainFrame object's properties and methods

        self.itemsText = tk.Text(self, height=20, width=190, state='disabled')  # Create the big textbox
        scrollBar = tk.Scrollbar(self, command=self.itemsText.yview)            # Create the scrollbar next to the big textbox
        self.itemsText['yscrollcommand'] = scrollBar.set                        # Link the scrollbar with the big textbox

        scrollBar.pack(side=tk.RIGHT, fill=tk.Y)                                # Draw big textbox on the right
        self.itemsText.pack(side=tk.LEFT)                                       # Draw scrollbar on the left

class StatsFrame(ttk.Frame):
    '''Frame that has the 3 stat entries'''
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.mainframe = parent # Easy way to access the MainFrame object's properties and methods
        # Create the entry boxes variables
        self.totalItems = tk.IntVar()
        self.totalAmount = tk.IntVar()
        self.totalPrice = tk.IntVar()
        # Grid padding and labels width
        _labelGrid = {"padx":2, "pady":0}
        _entryGrid = {"padx":2, "pady":0}
        _width = {"width":22}
        # Create the labels
        self.labelTotalItems = displayLabel(self, width=_width, text="Total item entries:")
        self.labelTotalAmount = displayLabel(self, width=_width, text="Total items amount:")
        self.labelTotalPrice = displayLabel(self, width=_width, text="Total items price: $")
        # Create the entry boxes
        self.entryTotalItems = displayEntry(self, textvariable=self.totalItems)
        self.entryTotalAmount = displayEntry(self, textvariable=self.totalAmount)
        self.entryTotalPrice = displayEntry(self, textvariable=self.totalPrice)

        self._entries = [self.entryTotalItems, self.entryTotalAmount, self.entryTotalPrice] # list of entries to iterate through later

        # Draw the labels and entry boxes
        self.labelTotalItems.grid(
            column=0, row=0, **_labelGrid
        )
        self.entryTotalItems.grid(
            column=1, row=0, **_entryGrid
        )
        self.labelTotalAmount.grid(
            column=2, row=0, **_labelGrid
        )
        self.entryTotalAmount.grid(
            column=3, row=0, **_entryGrid
        )
        self.labelTotalPrice.grid(
            column=4, row=0, **_labelGrid
        )
        self.entryTotalPrice.grid(
            column=5, row=0, **_entryGrid
        )

        for entry in self._entries:         # Set the list of entries to readonly
            entry['state'] = 'readonly'

class AddWindow(Toplevel):
    '''Opens new Add Item Window'''
    def __init__(self, parent, master=None):
        Toplevel.__init__(self, master) # Create the window on top of other windows
        self.parent = parent
        self.mainframe = parent # Easy way to access the MainFrame object's properties and methods
        self.title("Add Item")

        self.addItemFrame = AddItemFrame(self)

class AddItemFrame(ttk.Frame):
    '''Frame that as the Add item interface'''
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, borderwidth=5, relief="groove", padding="5 5 5 5")
        self.parent = parent
        self.mainframe = parent.mainframe   # Easy way to access the MainFrame object's properties and methods

        # Create entry box text variables
        self._itemIndex = tk.IntVar()
        self._itemName = tk.StringVar()
        self._itemLocation = tk.StringVar()
        self._itemAmount = tk.IntVar(value=1)
        self._itemPrice = tk.IntVar()

        self.initComponents()

    def initComponents(self):
        '''Initialize drawing of Add Item frame'''
        self.pack(fill=tk.BOTH, expand=True)    # Fill the frame's geometry for drawing
        # Create labels
        self.labelName = displayLabel(self, text="Name:")
        self.labelLocation = displayLabel(self, text="Location:")
        self.labelAmount = displayLabel(self, text="Amount:")
        self.labelPrice = displayLabel(self, text="Price: $")
        # Create entry boxes
        self.entryName = displayEntry(self, textvariable=self._itemName)
        self.entryLocation = displayEntry(self, textvariable=self._itemLocation)
        self.entryAmount = displayEntry(self, textvariable=self._itemAmount, validate='key', validatecommand=self.mainframe.vcmd)
        self.entryPrice = displayEntry(self, textvariable=self._itemPrice, validate='key', validatecommand=self.mainframe.vcmd)
        # Create buttons
        self.cancelButton = displayButton(self, text="Cancel", command=self.Cancel)
        self.enterButton = displayButton(self, text="Enter", command=self.AddItem)
        # Grid padding
        _labelGrid = {"padx":2, "pady":2}
        _entryGrid = {"padx":2, "pady":2}
        _buttonGrid = {"padx":2, "pady":2}
        # Draw labels, entry boxes and buttons
        self.labelName.grid(
            column=0, row=0, **_labelGrid
        )
        self.entryName.grid(
            column=1, row=0, **_entryGrid
        )
        self.labelLocation.grid(
            column=0, row=1, **_labelGrid
        )
        self.entryLocation.grid(
            column=1, row=1, **_entryGrid
        )
        self.labelAmount.grid(
            column=2, row=0, **_labelGrid
        )
        self.entryAmount.grid(
            column=3, row=0, **_entryGrid
        )
        self.labelPrice.grid(
            column=2, row=1, **_labelGrid
        )
        self.entryPrice.grid(
            column=3, row=1, **_entryGrid
        )
        self.cancelButton.grid(
            column=2, row=3, **_buttonGrid
        )
        self.enterButton.grid(
            column=3, row=3, **_buttonGrid
        )

    def Cancel(self):       # Close the window
        self.parent.destroy()

    def AddItem(self):      # Take entry box input, create Item object from that input, add it to the items list, refresh the big textbox and close the window
        self.mainframe._itemName = self._itemName.get()
        self.mainframe._itemLocation = self._itemLocation.get()
        self.mainframe._itemAmount = self._itemAmount.get()
        self.mainframe._itemPrice = self._itemPrice.get()
        self.mainframe._items.append(Item(name=self.mainframe._itemName, amount=self.mainframe._itemAmount, location=self.mainframe._itemLocation, price=self.mainframe._itemPrice))
        self.mainframe.RefreshDisplayData()
        self.parent.destroy()

class EditWindow(Toplevel):
    '''Opens the Edit Item Window'''
    def __init__(self, parent, master=None):
        Toplevel.__init__(self, master) # Create the window on top of other windows
        self.title("Edit Item")
        self.parent = parent
        self.mainframe = parent # Easy way to access the MainFrame object's properties and methods

        self.editItemFrame = EditItemFrame(self)

class EditItemFrame(ttk.Frame):
    '''Frame that has the Edit Item interface'''
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, borderwidth=5, relief="groove", padding="5 5 5 5")
        self.parent = parent
        self.mainframe = parent.mainframe   # Easy way to access the MainFrame object's properties and methods
        self._items = self.mainframe._items # Passing the items list from the MainFrame to this Frame
        # Create entry box text variables
        self._itemIndex = tk.IntVar()
        self._itemName = tk.StringVar()
        self._itemLocation = tk.StringVar()
        self._itemAmount = tk.IntVar()
        self._itemPrice = tk.IntVar()

        self.initComponents()

    def initComponents(self):
        '''Initialize drawing of Edit Item frame'''
        self.pack(fill=tk.BOTH, expand=True)    # Fills the frame's geometry for drawing
        # Create labels
        self.labelIndex = displayLabel(self, text="Item Index:")
        self.labelName = displayLabel(self, text="Name:")
        self.labelLocation = displayLabel(self, text="Location:")
        self.labelAmount = displayLabel(self, text="Amount:")
        self.labelPrice = displayLabel(self, text="Price: $")
        # Create combobox
        self.comboboxIndex = displayCombobox(self, textvariable=self._itemIndex)
        # Create entry boxes
        self.entryName = displayEntry(self, textvariable=self._itemName)
        self.entryLocation = displayEntry(self, textvariable=self._itemLocation)
        self.entryAmount = displayEntry(self, textvariable=self._itemAmount, validate='key', validatecommand=self.mainframe.vcmd)
        self.entryPrice = displayEntry(self, textvariable=self._itemPrice, validate='key', validatecommand=self.mainframe.vcmd)
        # Create the number of selectable combobox inputs from the amount of items in items list
        comboboxIndexValues = []
        for index, _item in enumerate(self._items):
            comboboxIndexValues.append(index+1)

        self.comboboxIndex['values'] = comboboxIndexValues  # Set combobox value to the amount of items
        self.comboboxIndex['state'] = 'readonly'            # Set combobox to readonly

        def ComboboxCallback(*args):                            # Update the entries displayed when the input changes in the combobox
            self.RefreshData(int(self.comboboxIndex.get())-1)
        self.comboboxIndex.bind("<<ComboboxSelected>>", ComboboxCallback)
        # create the Cancel and Enter button objects, "Cancel" to close the window and "Enter" to change the Item object's data to the new values
        self.cancelButton = displayButton(self, text="Cancel", command=self.Cancel)
        self.enterButton = displayButton(self, text="Enter", command=self.EditItem)
        # Grid padding
        _labelGrid = {"padx":2, "pady":2}
        _entryGrid = {"padx":2, "pady":2}
        _buttonGrid = {"padx":2, "pady":2}
        # Draw labels, combobox, entry boxes and buttons
        self.labelIndex.grid(
            column=0, row=0, columnspan=2, **_labelGrid
        )
        self.comboboxIndex.grid(
            column=2, row=0, columnspan=2, **_entryGrid
        )
        self.labelName.grid(
            column=0, row=1, **_labelGrid
        )
        self.entryName.grid(
            column=1, row=1, **_entryGrid
        )
        self.labelLocation.grid(
            column=0, row=2, **_labelGrid
        )
        self.entryLocation.grid(
            column=1, row=2, **_entryGrid
        )
        self.labelAmount.grid(
            column=2, row=1, **_labelGrid
        )
        self.entryAmount.grid(
            column=3, row=1, **_entryGrid
        )
        self.labelPrice.grid(
            column=2, row=2, **_labelGrid
        )
        self.entryPrice.grid(
            column=3, row=2, **_entryGrid
        )
        self.cancelButton.grid(
            column=2, row=3, **_buttonGrid
        )
        self.enterButton.grid(
            column=3, row=3, **_buttonGrid
        )

        self.RefreshData(0)

    def RefreshData(self, index):   # Fill in the data on the Edit Item window
        self.mainframe.RefreshInputData(self, index)

    def Cancel(self):       # Close the window
        self.parent.destroy()

    def EditItem(self):     # For the selected item in the combobox, change the data in the list for that indexed item, refresh the big textbox and close the window
        index = int(self.comboboxIndex.get()) - 1
        self._items[index].name = self.entryName.get()
        self._items[index].location = self.entryLocation.get()
        self._items[index].amount = round(float(self.entryAmount.get()), 0)
        self._items[index].price = self.entryPrice.get()
        self.mainframe.RefreshDisplayData()
        self.parent.destroy()

class DeleteWindow(Toplevel):
    '''Opens the Delete Item Window'''
    def __init__(self, parent, master=None):
        Toplevel.__init__(self, master) # Creates the Window on top of other windows
        self.title("Delete Item")
        self.parent = parent
        self.mainframe = parent # Easy way to access the MainFrame object's properties and methods

        self.deleteItemFrame = DeleteItemFrame(self)

class DeleteItemFrame(ttk.Frame):
    '''Frame that has the Delete Item interface'''
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, borderwidth=5, relief="groove", padding="5 5 5 5")
        self.parent = parent
        self.mainframe = parent.mainframe   # Easy way to access the MainFrame object's properties and methods
        self._items = self.mainframe._items # Passing the items list from the MainFrame to this Frame
        # Create the entry boxes variables
        self._itemIndex = tk.IntVar()
        self._itemName = tk.StringVar()
        self._itemLocation = tk.StringVar()
        self._itemAmount = tk.IntVar()
        self._itemPrice = tk.IntVar()

        self.initComponents()

    def initComponents(self):
        '''Initialize drawing of Delete Item frame'''
        self.pack(fill=tk.BOTH, expand=True)    # Fills the frame's geometry for drawing
        # Create labels
        self.labelIndex = displayLabel(self, text="Item Index:")
        self.labelName = displayLabel(self, text="Name:")
        self.labelLocation = displayLabel(self, text="Location:")
        self.labelAmount = displayLabel(self, text="Amount:")
        self.labelPrice = displayLabel(self, text="Price: $")
        # Create combobox
        self.comboboxIndex = displayCombobox(self, textvariable=self._itemIndex)
        # Create entry boxes
        self.entryName = displayEntry(self, textvariable=self._itemName)
        self.entryLocation = displayEntry(self, textvariable=self._itemLocation)
        self.entryAmount = displayEntry(self, textvariable=self._itemAmount)
        self.entryPrice = displayEntry(self, textvariable=self._itemPrice)
        self._entries = [self.entryName, self.entryLocation, self.entryAmount, self.entryPrice]
        for _entry in self._entries:
            _entry['state'] = 'readonly'
        # Create the number of selectable combobox inputs from the amount of items in items list
        comboboxIndexValues = []
        for index, _item in enumerate(self._items):
            comboboxIndexValues.append(index+1)
        self.comboboxIndex['values'] = comboboxIndexValues  # Set combobox value to the amount of items
        self.comboboxIndex['state'] = 'readonly'            # Set combobox to readonly

        def ComboboxCallback(*args):                # Update the entries displayed when the input changes in the combobox
            self.RefreshData(int(self.comboboxIndex.get())-1)
        self.comboboxIndex.bind("<<ComboboxSelected>>", ComboboxCallback)
        # create the Cancel and Enter button objects, "Cancel" to close the window and "Enter" to delete the selected Item from the items list 
        self.cancelButton = displayButton(self, text="Cancel", command=self.Cancel)
        self.enterButton = displayButton(self, text="Enter", command=self.DeleteItem)
        # Grid padding
        _labelGrid = {"padx":2, "pady":2}
        _entryGrid = {"padx":2, "pady":2}
        _buttonGrid = {"padx":2, "pady":2}
        # Draw labels, combobox, entry boxes and buttons
        self.labelIndex.grid(
            column=0, row=0, columnspan=2, **_labelGrid
        )
        self.comboboxIndex.grid(
            column=2, row=0, columnspan=2, **_entryGrid
        )
        self.labelName.grid(
            column=0, row=1, **_labelGrid
        )
        self.entryName.grid(
            column=1, row=1, **_entryGrid
        )
        self.labelLocation.grid(
            column=0, row=2, **_labelGrid
        )
        self.entryLocation.grid(
            column=1, row=2, **_entryGrid
        )
        self.labelAmount.grid(
            column=2, row=1, **_labelGrid
        )
        self.entryAmount.grid(
            column=3, row=1, **_entryGrid
        )
        self.labelPrice.grid(
            column=2, row=2, **_labelGrid
        )
        self.entryPrice.grid(
            column=3, row=2, **_entryGrid
        )
        self.cancelButton.grid(
            column=2, row=3, **_buttonGrid
        )
        self.enterButton.grid(
            column=3, row=3, **_buttonGrid
        )

        self.RefreshData(0)

    def RefreshData(self, index):       # Set the entry boxes to a writable state, fill in the data on the Delete Item window and make them readonly again
        for _entry in self._entries:
            _entry['state'] = 'normal'

        self.mainframe.RefreshInputData(self, index)

        for _entry in self._entries:
            _entry['state'] = 'readonly'

    def Cancel(self):           # Close the window
        self.parent.destroy()

    def DeleteItem(self):       # For the selected item in the combobox, delete that item in the list, refresh the big text and close the window
        index = int(self.comboboxIndex.get()) - 1
        del self._items[index]
        self.mainframe.RefreshDisplayData()
        self.parent.destroy()

class displayLabel(ttk.Label):
    '''A label with custom defaults'''
    def __init__(self, parent, width=25, anchor="e", relief=tk.FLAT, **kwargs):
        ttk.Label.__init__(self, parent, width=width, anchor=anchor, relief=relief, **kwargs)
        self.parent = parent

class displayEntry(ttk.Entry):
    '''An entry box with custom defaults
       Also allows setting text via its "set_text" method'''
    def __init__(self, parent, width=40, **kwargs):
        ttk.Entry.__init__(self, parent, width=width, **kwargs)
        self.parent = parent

    def set_text(self, text):   # Clear the text field, add the new text
        self.delete(0,'end')
        self.insert(0,text)

class displayCombobox(ttk.Combobox):
    '''A combobox with custom defaults'''
    def __init__(self, parent, width=40, **kwargs):
        ttk.Combobox.__init__(self, parent, width=width, **kwargs)
        self.parent = parent

class displayButton(ttk.Button):
    '''A button with custom defaults'''
    def __init__(self, parent, width=30, padding="5 5 5 5", **kwargs):
        ttk.Button.__init__(self, parent, width=width, padding=padding, **kwargs)
        self.parent = parent

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(0, 0)                    # Window is not resizable
    root.title("Minimalist Item Tracker")
    MainFrame(root)
    root.mainloop()
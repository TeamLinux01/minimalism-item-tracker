#!/bin/python3

import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from modules.tracker import Item

class MainFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="2 2 2 2")
        self.parent = parent
        self.textFrame = TextFrame(self)
        self.commandFrame = CommandFrame(self)

        self._itemName = ""
        self._itemLocation = ""
        self._itemAmount = 0
        self._itemPrice = 0

        self._items = []

        self.initComponents()

    def initComponents(self):
        self.pack(fill=tk.BOTH, expand=True)

        self.commandFrame.grid(
            column=0, row=0
        )
        self.textFrame.grid(
            column=0, row=1
        )

class CommandFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, borderwidth=5, relief="groove", padding="5 5 5 5")
        self.parent = parent
        self.mainframe = parent
   
        self.initComponents()

    def initComponents(self):

        _gridGrid = {"padx":100, "pady":5}
        
        self.addItemButton = displayButton(self, text="Add Item", command=self.AddItem).grid(
            column=0, row=0, **_gridGrid
        )
        self.editItemButton = displayButton(self, text="Edit Item", command=self.EditItem).grid(
            column=0, row=1, **_gridGrid
        )
        self.deleteItemButton = displayButton(self, text="Delete Item", command=self.DeleteItem).grid(
            column=0, row=2, **_gridGrid
        )
    
    def AddItem(self):
        self.addWindow = AddWindow(self.mainframe, master=root).resizable(0, 0)

    def EditItem(self):
        self.editWindow = EditWindow(master=root).resizable(0, 0)
    
    def DeleteItem(self):
        self.deleteWindow = DeleteWindow(master=root).resizable(0, 0)

class TextFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.mainframe = parent

        self.itemsText = tk.Text(self, height=20, width=190, state='disabled')
        scrollBar = tk.Scrollbar(self, command=self.itemsText.yview)
        self.itemsText['yscrollcommand'] = scrollBar.set

        scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        self.itemsText.pack(side=tk.LEFT)

    def UpdateText(self):
        self.parent._items.append(Item(self.parent._itemName, self.parent._itemLocation, self.parent._itemAmount, self.parent._itemPrice))
        self.itemsText.configure(state='normal')
        self.itemsText.delete('1.0', 'end')
        self.itemsText.insert('end', self.parent._items)
        self.itemsText.configure(state='disabled')

class AddWindow(Toplevel):
    def __init__(self, parent, master=None):
        Toplevel.__init__(self, master)
        self.parent = parent
        self.mainframe = parent
        self.title("Add Item")

        self.addItemFrame = AddItemFrame(self)

class AddItemFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, borderwidth=5, relief="groove", padding="5 5 5 5")
        self.parent = parent
        self.mainframe = parent.mainframe

        self._itemIndex = tk.IntVar()
        self._itemName = tk.StringVar()
        self._itemLocation = tk.StringVar()
        self._itemAmount = tk.IntVar(value=1)
        self._itemPrice = tk.IntVar()

        self.initComponents()

    def initComponents(self):
        self.pack(fill=tk.BOTH, expand=True)

        vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.nameLabel = displayLabel(self, text="Name:")
        self.locationLabel = displayLabel(self, text="Location:")
        self.amountLabel = displayLabel(self, text="Amount:")
        self.priceLabel = displayLabel(self, text="Price:")

        self.entryName = displayEntry(self, textvariable=self._itemName)
        self.entryLocation = displayEntry(self, textvariable=self._itemLocation)
        self.entryAmount = displayEntry(self, textvariable=self._itemAmount, validate='key', validatecommand=vcmd)
        self.entryPrice = displayEntry(self, textvariable=self._itemPrice, validate='key', validatecommand=vcmd)

        self.cancelButton = displayButton(self, text="Cancel", command=self.Cancel)
        self.enterButton = displayButton(self, text="Enter", command=self.AddItem)

        _labelGrid = {"padx":2, "pady":2}
        _entryGrid = {"padx":2, "pady":2}
        _buttonGrid = {"padx":2, "pady":2}

        self.nameLabel.grid(
            column=0, row=0, **_labelGrid
        )
        self.entryName.grid(
            column=1, row=0, **_entryGrid
        )

        self.locationLabel.grid(
            column=0, row=1, **_labelGrid
        )
        self.entryLocation.grid(
            column=1, row=1, **_entryGrid
        )

        self.amountLabel.grid(
            column=2, row=0, **_labelGrid
        )
        self.entryAmount.grid(
            column=3, row=0, **_entryGrid
        )

        self.priceLabel.grid(
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

    def validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed:
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

    def Cancel(self):
        self.parent.destroy()

    def AddItem(self):
        self.mainframe._itemName = self._itemName.get()
        self.mainframe._itemLocation = self._itemLocation.get()
        self.mainframe._itemAmount = self._itemAmount.get()
        self.mainframe._itemPrice = self._itemPrice.get()
        self.mainframe.textFrame.UpdateText()

class EditWindow(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master)
        self.title("Edit Item")

        self.editItemFrame = EditItemFrame(self)

class EditItemFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, borderwidth=5, relief="groove", padding="5 5 5 5")
        self.parent = parent

        self._itemIndex = tk.IntVar()
        self._itemName = tk.StringVar()
        self._itemLocation = tk.StringVar()
        self._itemAmount = tk.IntVar(value=1)
        self._itemPrice = tk.IntVar()

        self.initComponents()

    def initComponents(self):
        self.pack(fill=tk.BOTH, expand=True)

        vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.indexLabel = displayLabel(self, text="Item Index:")
        self.nameLabel = displayLabel(self, text="Name:")
        self.locationLabel = displayLabel(self, text="Location:")
        self.amountLabel = displayLabel(self, text="Amount:")
        self.priceLabel = displayLabel(self, text="Price:")

        self.indexCombobox = displayCombobox(self, textvariable=self._itemIndex)

        self.entryName = displayEntry(self, textvariable=self._itemName)
        self.entryLocation = displayEntry(self, textvariable=self._itemLocation)
        self.entryAmount = displayEntry(self, textvariable=self._itemAmount, validate='key', validatecommand=vcmd)
        self.entryPrice = displayEntry(self, textvariable=self._itemPrice, validate='key', validatecommand=vcmd)

        self.indexCombobox['values'] = ('1', '2', '3')
        self.indexCombobox['state'] = 'readonly'

        self.cancelButton = displayButton(self, text="Cancel", command=self.Cancel)
        self.enterButton = displayButton(self, text="Enter")

        _labelGrid = {"padx":2, "pady":2}
        _entryGrid = {"padx":2, "pady":2}
        _buttonGrid = {"padx":2, "pady":2}

        self.indexLabel.grid(
            column=0, row=0, columnspan=2, **_labelGrid
        )
        self.indexCombobox.grid(
            column=2, row=0, columnspan=2, **_entryGrid
        )

        self.nameLabel.grid(
            column=0, row=1, **_labelGrid
        )
        self.entryName.grid(
            column=1, row=1, **_entryGrid
        )

        self.locationLabel.grid(
            column=0, row=2, **_labelGrid
        )
        self.entryLocation.grid(
            column=1, row=2, **_entryGrid
        )

        self.amountLabel.grid(
            column=2, row=1, **_labelGrid
        )
        self.entryAmount.grid(
            column=3, row=1, **_entryGrid
        )

        self.priceLabel.grid(
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

    def validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed:
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

    def Cancel(self):
        self.parent.destroy()

class DeleteWindow(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master)
        self.title("Delete Item")

        self.deleteItemFrame = DeleteItemFrame(self)

class DeleteItemFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, borderwidth=5, relief="groove", padding="5 5 5 5")
        self.parent = parent

        self._itemIndex = tk.IntVar()
        self._itemName = tk.StringVar()
        self._itemLocation = tk.StringVar()
        self._itemAmount = tk.IntVar(value=1)
        self._itemPrice = tk.IntVar()

        self.initComponents()

    def initComponents(self):
        self.pack(fill=tk.BOTH, expand=True)

        self.indexLabel = displayLabel(self, text="Item Index:")
        self.nameLabel = displayLabel(self, text="Name:")
        self.locationLabel = displayLabel(self, text="Location:")
        self.amountLabel = displayLabel(self, text="Amount:")
        self.priceLabel = displayLabel(self, text="Price:")

        self.indexCombobox = displayCombobox(self, textvariable=self._itemIndex)

        self.entryName = displayEntry(self, textvariable=self._itemName)
        self.entryLocation = displayEntry(self, textvariable=self._itemLocation)
        self.entryAmount = displayEntry(self, textvariable=self._itemAmount)
        self.entryPrice = displayEntry(self, textvariable=self._itemPrice)
        _entries = [self.entryName, self.entryLocation, self.entryAmount, self.entryPrice]
        for _entry in _entries:
            _entry['state'] = 'readonly'

        self.indexCombobox['values'] = ('1', '2', '3')
        self.indexCombobox['state'] = 'readonly'

        self.cancelButton = displayButton(self, text="Cancel", command=self.Cancel)
        self.enterButton = displayButton(self, text="Enter")

        _labelGrid = {"padx":2, "pady":2}
        _entryGrid = {"padx":2, "pady":2}
        _buttonGrid = {"padx":2, "pady":2}

        self.indexLabel.grid(
            column=0, row=0, columnspan=2, **_labelGrid
        )
        self.indexCombobox.grid(
            column=2, row=0, columnspan=2, **_entryGrid
        )

        self.nameLabel.grid(
            column=0, row=1, **_labelGrid
        )
        self.entryName.grid(
            column=1, row=1, **_entryGrid
        )

        self.locationLabel.grid(
            column=0, row=2, **_labelGrid
        )
        self.entryLocation.grid(
            column=1, row=2, **_entryGrid
        )

        self.amountLabel.grid(
            column=2, row=1, **_labelGrid
        )
        self.entryAmount.grid(
            column=3, row=1, **_entryGrid
        )

        self.priceLabel.grid(
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

    def Cancel(self):
        self.parent.destroy()

class displayLabel(ttk.Label):
    def __init__(self, parent, width=25, anchor="e", relief=tk.FLAT, **kw):
        ttk.Label.__init__(self, parent, width=width, anchor=anchor, relief=relief, **kw)
        self.parent = parent

class displayEntry(ttk.Entry):
    def __init__(self, parent, width=40, **kw):
        ttk.Entry.__init__(self, parent, width=width, **kw)
        self.parent = parent

class displayCombobox(ttk.Combobox):
    def __init__(self, parent, width=40, **kw):
        ttk.Combobox.__init__(self, parent, width=width, **kw)
        self.parent = parent

class displayButton(ttk.Button):
    def __init__(self, parent, width=30, padding="5 5 5 5", **kw):
        ttk.Button.__init__(self, parent, width=width, padding=padding, **kw)
        self.parent = parent

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(0, 0)
    root.title("Minimalist Item Tracker")
    MainFrame(root)
    root.mainloop()
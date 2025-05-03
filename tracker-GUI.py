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

        self._items = [Item("Computer", "Office", 1, 2000), Item("Spoon", "Kitchen", 10, 2), Item("TV", "Livingroom", 1, 1000)]
        self.RefreshTextbox()

        self.initComponents()

    def initComponents(self):
        self.pack(fill=tk.BOTH, expand=True)

        self.commandFrame.grid(
            column=0, row=0
        )
        self.textFrame.grid(
            column=0, row=1
        )

    def RefreshTextbox(self):
        self.textFrame.itemsText.configure(state='normal')
        self.textFrame.itemsText.delete('1.0', 'end')
        for _item in self._items:
            self.textFrame.itemsText.insert('end', _item)
            self.textFrame.itemsText.insert('end', '\n')

        self.textFrame.itemsText.configure(state='disabled')

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
        self.editWindow = EditWindow(self.mainframe, master=root).resizable(0, 0)
    
    def DeleteItem(self):
        self.deleteWindow = DeleteWindow(self.mainframe, master=root).resizable(0, 0)

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

        self.labelName = displayLabel(self, text="Name:")
        self.labelLocation = displayLabel(self, text="Location:")
        self.labelAmount = displayLabel(self, text="Amount:")
        self.labelPrice = displayLabel(self, text="Price:")

        self.entryName = displayEntry(self, textvariable=self._itemName)
        self.entryLocation = displayEntry(self, textvariable=self._itemLocation)
        self.entryAmount = displayEntry(self, textvariable=self._itemAmount, validate='key', validatecommand=vcmd)
        self.entryPrice = displayEntry(self, textvariable=self._itemPrice, validate='key', validatecommand=vcmd)

        self.cancelButton = displayButton(self, text="Cancel", command=self.Cancel)
        self.enterButton = displayButton(self, text="Enter", command=self.AddItem)

        _labelGrid = {"padx":2, "pady":2}
        _entryGrid = {"padx":2, "pady":2}
        _buttonGrid = {"padx":2, "pady":2}

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
        self.mainframe._items.append(Item(self.mainframe._itemName, self.mainframe._itemLocation, self.mainframe._itemAmount, self.mainframe._itemPrice))
        self.mainframe.RefreshTextbox()
        self.parent.destroy()

class EditWindow(Toplevel):
    def __init__(self, parent, master=None):
        Toplevel.__init__(self, master)
        self.title("Edit Item")
        self.parent = parent
        self.mainframe = parent

        self.editItemFrame = EditItemFrame(self)

class EditItemFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, borderwidth=5, relief="groove", padding="5 5 5 5")
        self.parent = parent
        self.mainframe = parent.mainframe
        self._items = self.mainframe._items


        self._itemIndex = tk.IntVar()
        self._itemName = tk.StringVar()
        self._itemLocation = tk.StringVar()
        self._itemAmount = tk.IntVar()
        self._itemPrice = tk.IntVar()

        self.initComponents()

    def initComponents(self):
        self.pack(fill=tk.BOTH, expand=True)

        vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.labelIndex = displayLabel(self, text="Item Index:")
        self.labelName = displayLabel(self, text="Name:")
        self.labelLocation = displayLabel(self, text="Location:")
        self.labelAmount = displayLabel(self, text="Amount:")
        self.labelPrice = displayLabel(self, text="Price:")

        self.comboboxIndex = displayCombobox(self, textvariable=self._itemIndex)

        self.entryName = displayEntry(self, textvariable=self._itemName)
        self.entryLocation = displayEntry(self, textvariable=self._itemLocation)
        self.entryAmount = displayEntry(self, textvariable=self._itemAmount, validate='key', validatecommand=vcmd)
        self.entryPrice = displayEntry(self, textvariable=self._itemPrice, validate='key', validatecommand=vcmd)

        comboboxIndexValues = []
        i = 1
        for _item in self._items:
            comboboxIndexValues.append(i)
            i += 1

        self.comboboxIndex['values'] = comboboxIndexValues
        self.comboboxIndex['state'] = 'readonly'

        def callback(*args):
            self.RefreshData(int(self.comboboxIndex.get())-1)

        self.comboboxIndex.bind("<<ComboboxSelected>>", callback)

        self.cancelButton = displayButton(self, text="Cancel", command=self.Cancel)
        self.enterButton = displayButton(self, text="Enter", command=self.EditItem)

        _labelGrid = {"padx":2, "pady":2}
        _entryGrid = {"padx":2, "pady":2}
        _buttonGrid = {"padx":2, "pady":2}

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

    def RefreshData(self, index):
        i = index
        self._itemIndex = i+1
        self.comboboxIndex.set(self._itemIndex)
        self._itemName = self._items[i].name
        self.entryName.set_text(self._itemName)
        self._itemLocation = self._items[i].location
        self.entryLocation.set_text(self._itemLocation)
        self._itemAmount = self._items[i].amount
        self.entryAmount.set_text(self._itemAmount)
        self._itemPrice = self._items[i].price
        self.entryPrice.set_text(self._itemPrice)

    def validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed:
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        elif value_if_allowed is "":
            return True
        else:
            return False

    def Cancel(self):
        self.parent.destroy()

    def EditItem(self):
        index = int(self.comboboxIndex.get()) - 1
        self._items[index].name = self.entryName.get()
        self._items[index].location = self.entryLocation.get()
        self._items[index].amount = self.entryAmount.get()
        self._items[index].price = self.entryPrice.get()
        self.mainframe.RefreshTextbox()
        self.parent.destroy()

class DeleteWindow(Toplevel):
    def __init__(self, parent, master=None):
        Toplevel.__init__(self, master)
        self.title("Delete Item")
        self.parent = parent
        self.mainframe = parent

        self.deleteItemFrame = DeleteItemFrame(self)

class DeleteItemFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, borderwidth=5, relief="groove", padding="5 5 5 5")
        self.parent = parent
        self.mainframe = parent.mainframe
        self._items = self.mainframe._items

        self._itemIndex = tk.IntVar()
        self._itemName = tk.StringVar()
        self._itemLocation = tk.StringVar()
        self._itemAmount = tk.IntVar(value=1)
        self._itemPrice = tk.IntVar()

        self.initComponents()

    def initComponents(self):
        self.pack(fill=tk.BOTH, expand=True)

        self.labelIndex = displayLabel(self, text="Item Index:")
        self.labelName = displayLabel(self, text="Name:")
        self.labelLocation = displayLabel(self, text="Location:")
        self.labelAmount = displayLabel(self, text="Amount:")
        self.labelPrice = displayLabel(self, text="Price:")

        self.comboboxIndex = displayCombobox(self, textvariable=self._itemIndex)

        self.entryName = displayEntry(self, textvariable=self._itemName)
        self.entryLocation = displayEntry(self, textvariable=self._itemLocation)
        self.entryAmount = displayEntry(self, textvariable=self._itemAmount)
        self.entryPrice = displayEntry(self, textvariable=self._itemPrice)
        self._entries = [self.entryName, self.entryLocation, self.entryAmount, self.entryPrice]
        for _entry in self._entries:
            _entry['state'] = 'readonly'

        comboboxIndexValues = []
        i = 1
        for _item in self._items:
            comboboxIndexValues.append(i)
            i += 1

        self.comboboxIndex['values'] = comboboxIndexValues
        self.comboboxIndex['state'] = 'readonly'

        def callback(*args):
            self.RefreshData(int(self.comboboxIndex.get())-1)

        self.comboboxIndex.bind("<<ComboboxSelected>>", callback)

        self.cancelButton = displayButton(self, text="Cancel", command=self.Cancel)
        self.enterButton = displayButton(self, text="Enter", command=self.DeleteItem)

        _labelGrid = {"padx":2, "pady":2}
        _entryGrid = {"padx":2, "pady":2}
        _buttonGrid = {"padx":2, "pady":2}

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

    def RefreshData(self, index):
        for _entry in self._entries:
            _entry['state'] = 'normal'

        i = index
        self._itemIndex = i+1
        self.comboboxIndex.set(self._itemIndex)
        self._itemName = self._items[i].name
        self.entryName.set_text(self._itemName)
        self._itemLocation = self._items[i].location
        self.entryLocation.set_text(self._itemLocation)
        self._itemAmount = self._items[i].amount
        self.entryAmount.set_text(self._itemAmount)
        self._itemPrice = self._items[i].price
        self.entryPrice.set_text(self._itemPrice)

        for _entry in self._entries:
            _entry['state'] = 'readonly'

    def Cancel(self):
        self.parent.destroy()

    def DeleteItem(self):
        index = int(self.comboboxIndex.get()) - 1
        del self._items[index]
        self.mainframe.RefreshTextbox()
        self.parent.destroy()

class displayLabel(ttk.Label):
    def __init__(self, parent, width=25, anchor="e", relief=tk.FLAT, **kw):
        ttk.Label.__init__(self, parent, width=width, anchor=anchor, relief=relief, **kw)
        self.parent = parent

class displayEntry(ttk.Entry):
    def __init__(self, parent, width=40, **kw):
        ttk.Entry.__init__(self, parent, width=width, **kw)
        self.parent = parent

    def set_text(self, text):
        self.delete(0,'end')
        self.insert(0,text)

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
#!/bin/python3

import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from modules.tracker import Item

class MainFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="2 2 2 2")
        self.parent = parent
        self.textFrame = TextFrame(self)
        self.itemFrame = AddItemFrame(self)

        self._itemName = ""
        self._itemLocation = ""
        self._itemAmount = 0
        self._itemPrice = 0

        global _rowNumber 
        _rowNumber = 0

        self._items = []

        self.initComponents()

    def initComponents(self):
        self.pack(fill=tk.BOTH, expand=True)

        self.itemFrame.grid(
            column=0, row=0
        )

        self.textFrame.grid(
            column=0, row=1
        )

class AddItemFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, borderwidth=5, relief="groove", padding="5 5 5 5")
        self.parent = parent

        self._itemName = tk.StringVar()
        self._itemLocation = tk.StringVar()
        self._itemAmount = tk.IntVar(value=1)
        self._itemPrice = tk.IntVar()

        self.initComponents()

    def initComponents(self):
        self.pack(fill=tk.BOTH, expand=True)

        vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        _labelWidth = 21
        _labelPadx = 2
        _labelPady = 2
        _labelAnchor = "e"
        _labelRelief = tk.FLAT
        _entryWidth = 40
        _entryPadx = 2
        _entryPady = 2

        ttk.Label(self, width=_labelWidth, anchor=_labelAnchor, relief=_labelRelief, text="Name:").grid(
            column=0, row=0, padx=_labelPadx, pady=_labelPady
        )
        ttk.Entry(self, width=_entryWidth, textvariable=self._itemName).grid(
            column=1, row=0, padx=_entryPadx, pady=_entryPady
        )

        ttk.Label(self, width=_labelWidth, anchor=_labelAnchor, relief=_labelRelief, text="Location:").grid(
            column=0, row=1, padx=_labelPadx, pady=_labelPady
        )
        ttk.Entry(self, width=_entryWidth, textvariable=self._itemLocation).grid(
            column=1, row=1, padx=_entryPadx, pady=_entryPady
        )

        ttk.Label(self, width=_labelWidth, anchor=_labelAnchor, relief=_labelRelief, text="Amount:").grid(
            column=2, row=0, padx=_labelPadx, pady=_labelPady
        )
        ttk.Entry(self, width=_entryWidth, textvariable=self._itemAmount, validate='key', validatecommand=vcmd).grid(
            column=3, row=0, padx=_entryPadx, pady=_entryPady
        )

        ttk.Label(self, width=_labelWidth, anchor=_labelAnchor, relief=_labelRelief, text="Price:").grid(
            column=2, row=1, padx=_labelPadx, pady=_labelPady
        )
        ttk.Entry(self, width=_entryWidth, textvariable=self._itemPrice, validate='key', validatecommand=vcmd).grid(
            column=3, row=1, padx=_entryPadx
        )

        self.makeButtons()

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

    def makeButtons(self):

        _buttonWidth = 30
        _buttonPadding = "5 5 5 5"
        _gridPadx = 100
        _gridPady = 5
        ttk.Button(self, text="Add Item", width=_buttonWidth, padding=_buttonPadding, command=self.AddItem).grid(
            column=4, row=0, padx=_gridPadx, pady=_gridPady
        )
        ttk.Button(self, text="Edit Item", width=_buttonWidth, padding=_buttonPadding).grid(
            column=4, row=1, padx=_gridPadx, pady=_gridPady
        )
        ttk.Button(self, text="Delete Item", width=_buttonWidth, padding=_buttonPadding).grid(
            column=4, row=2, padx=_gridPadx, pady=_gridPady
        )

    def AddItem(self):
        self.parent._itemName = self._itemName.get()
        self.parent._itemLocation = self._itemLocation.get()
        self.parent._itemAmount = self._itemAmount.get()
        self.parent._itemPrice = self._itemPrice.get()
        self.parent.textFrame.UpdateText()

class TextFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent

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

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minimalist Item Tracker")
    MainFrame(root)
    root.mainloop()
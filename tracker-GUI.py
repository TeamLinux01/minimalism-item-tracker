#!/bin/python3

import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from modules.tracker import Item

class MainFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="2 2 2 2")
        self.parent = parent

        global _rowNumber 
        _rowNumber = 0

        global _items
        _items = []

        self.initComponents()

    def initComponents(self):
        self.pack(fill=tk.BOTH, expand=True)

        AddItemFrame(self).grid(
            column=0, row=0
        )

        TextFrame(self).grid(
            column=0, row=1
        )



class AddItemFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, borderwidth=5, relief="groove", padding="5 5 5 5")
        self.parent = parent

        self._itemName = tk.StringVar()
        self._itemLocation = tk.StringVar()
        self._itemAmount = tk.StringVar()
        self._itemInHome = tk.StringVar()
        self._itemPrice = tk.StringVar()
        self._itemUpc = tk.StringVar()
        self._itemStillOwned = tk.StringVar()

        self.initComponents()

    def initComponents(self):
        self.pack(fill=tk.BOTH, expand=True)

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
            column=0, row=2, padx=_labelPadx, pady=_labelPady
        )
        ttk.Entry(self, width=_entryWidth, textvariable=self._itemAmount).grid(
            column=1, row=2, padx=_entryPadx, pady=_entryPady
        )

        ttk.Label(self, width=_labelWidth, anchor=_labelAnchor, relief=_labelRelief, text="Date brought in home:").grid(
            column=2, row=0, padx=_labelPadx, pady=_labelPady
        )
        ttk.Entry(self, width=_entryWidth, textvariable=self._itemInHome).grid(
            column=3, row=0, padx=_entryPadx, pady=_entryPady
        )

        ttk.Label(self, width=_labelWidth, anchor=_labelAnchor, relief=_labelRelief, text="Price:").grid(
            column=2, row=1, padx=_labelPadx, pady=_labelPady
        )
        ttk.Entry(self, width=_entryWidth, textvariable=self._itemPrice).grid(
            column=3, row=1, padx=_entryPadx
        )

        ttk.Label(self, width=_labelWidth, anchor=_labelAnchor, relief=_labelRelief, text="UPC:").grid(
            column=2, row=2, padx=_labelPadx, pady=_labelPady
        )
        ttk.Entry(self, width=_entryWidth, textvariable=self._itemUpc).grid(
            column=3, row=2, padx=_entryPadx, pady=_entryPady
        )

        self.makeButtons()

    def makeButtons(self):

        _buttonWidth = 30
        _buttonPadding = "5 5 5 5"
        _gridPadx = 100
        _gridPady = 5
        ttk.Button(self, text="Add Item", width=_buttonWidth, padding=_buttonPadding).grid(
            column=4, row=0, padx=_gridPadx, pady=_gridPady
        )
        ttk.Button(self, text="Edit Item", width=_buttonWidth, padding=_buttonPadding).grid(
            column=4, row=1, padx=_gridPadx, pady=_gridPady
        )
        ttk.Button(self, text="Delete Item", width=_buttonWidth, padding=_buttonPadding).grid(
            column=4, row=2, padx=_gridPadx, pady=_gridPady
        )

class TextFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent

        itemsText = tk.Text(self, height=20, width=190)
        scrollBar = tk.Scrollbar(self, command=itemsText.yview)
        itemsText['yscrollcommand'] = scrollBar.set

        scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        itemsText.pack(side=tk.LEFT)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minimalist Item Tracker")
    MainFrame(root)
    root.mainloop()
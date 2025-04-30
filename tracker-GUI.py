#!/bin/python3

import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from modules.tracker import Item, Location

class MainFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="2 10 10 2")
        self.parent = parent

        global _rowNumber 
        _rowNumber = 0

        self.initComponents()

    def initComponents(self):
        self.pack(fill=tk.BOTH, expand=True)

        HeaderFrame(self).grid(
            column=0, row=0
        )

        _listFrame = listFrame(self).grid(
            column=0, row=1
        )

        self.makeButtons()

        for child in self.winfo_children():
            child.grid_configure(padx=1)

    def makeButtons(self):
        buttonFrame = ttk.Frame(self)
        buttonFrame.grid(column=1, row=10)

        ttk.Button(buttonFrame, text="Add Item", command=self.addItemWindow) \
            .grid(column=0, row=0)
        
    def addItemWindow(self):
        _addWindow = Toplevel(root)
        _addWindow.title("Add Item")
        _addWindow.frame = AddItemFrame(_addWindow).pack
        
class AddItemFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="2 10 10 2")
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

        _entryWidth=30

        ttk.Entry(self, width=_entryWidth, textvariable=self._itemName).grid(
            column=0, row=0
        )
        ttk.Entry(self, width=_entryWidth, textvariable=self._itemLocation).grid(
            column=1, row=0
        )
        ttk.Entry(self, width=_entryWidth, textvariable=self._itemAmount).grid(
            column=2, row=0
        )
        ttk.Entry(self, width=_entryWidth, textvariable=self._itemInHome).grid(
            column=3, row=0
        )
        ttk.Entry(self, width=_entryWidth, textvariable=self._itemPrice).grid(
            column=4, row=0
        )
        ttk.Entry(self, width=_entryWidth, textvariable=self._itemUpc).grid(
            column=5, row=0
        )
        ttk.Entry(self, width=_entryWidth, textvariable=self._itemStillOwned).grid(
            column=6, row=0
        )

class HeaderFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent

        self.initComponents()

    def initComponents(self):
        self.pack(fill=tk.BOTH, expand=True)

        labelWidth = 30
        labelJustify = tk.CENTER
        labelRelief = tk.RAISED

        ttk.Label(self, width=labelWidth, justify=labelJustify, relief=labelRelief, text="Name").grid(
            column=0, row=0
        )
        ttk.Label(self, width=labelWidth, justify=labelJustify, relief=labelRelief, text="Location").grid(
            column=1, row=0
        )
        ttk.Label(self, width=labelWidth, justify=labelJustify, relief=labelRelief, text="Amount").grid(
            column=2, row=0
        )
        ttk.Label(self, width=labelWidth, justify=labelJustify, relief=labelRelief, text="Date brought in home").grid(
            column=3, row=0
        )
        ttk.Label(self, width=labelWidth, justify=labelJustify, relief=labelRelief, text="Price").grid(
            column=4, row=0
        )
        ttk.Label(self, width=labelWidth, justify=labelJustify, relief=labelRelief, text="UPC").grid(
            column=5, row=0
        )
        ttk.Label(self, width=labelWidth, justify=labelJustify, relief=labelRelief, text="Still Owned?").grid(
            column=6, row=0
        )

class listFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self._parent = parent

        self.initComponents()

    def initComponents(self):
        global _rowNumber
        _framelist = []
        for i in range(10):
            _framelist.append(ItemFrame(self).grid(
                column=0, row=_rowNumber
            ))
            _rowNumber += 1


class ItemFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self._parent = parent        

        self._itemName = tk.StringVar()
        self._itemLocation = tk.StringVar()
        self._itemAmount = tk.StringVar()
        self._itemInHome = tk.StringVar()
        self._itemPrice = tk.StringVar()
        self._itemUpc = tk.StringVar()
        self._itemStillOwned = tk.StringVar()

        self._itemName.set(_rowNumber)

        self.initComponents()
        
    def initComponents(self):
        _entryWidth=30

        ttk.Entry(self, width=_entryWidth, textvariable=self._itemName, state="readonly").grid(
            column=0, row=0
        )
        ttk.Entry(self, width=_entryWidth, textvariable=self._itemLocation, state="readonly").grid(
            column=1, row=0
        )
        ttk.Entry(self, width=_entryWidth, textvariable=self._itemAmount, state="readonly").grid(
            column=2, row=0
        )
        ttk.Entry(self, width=_entryWidth, textvariable=self._itemInHome, state="readonly").grid(
            column=3, row=0
        )
        ttk.Entry(self, width=_entryWidth, textvariable=self._itemPrice, state="readonly").grid(
            column=4, row=0
        )
        ttk.Entry(self, width=_entryWidth, textvariable=self._itemUpc, state="readonly").grid(
            column=5, row=0
        )
        ttk.Entry(self, width=_entryWidth, textvariable=self._itemStillOwned, state="readonly").grid(
            column=6, row=0
        )
            
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minimalist Item Tracker")
    MainFrame(root)
    root.mainloop()
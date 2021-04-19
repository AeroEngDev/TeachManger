import tkinter as tk
import tkinter.ttk as ttk


class excel_export_window:

    def __init__(self):

        self.window = tk.Tk()
        self.create_tree()
        self.window.mainloop()

    def create_tree(self):
        my_tree = ttk.Treeview(self.window)

        # Define Columns:
        my_tree['columns'] = ("ID", "Vorname", "Nachname", "Note 1")

        # Format your columns
        # hidden column is called "#0"
        my_tree.column("#0", width=120, minwidth=25, anchor=tk.W)
        my_tree.column("ID", anchor=tk.W)
        my_tree.column("Vorname", anchor=tk.CENTER)
        my_tree.column("Nachname", anchor=tk.CENTER)
        my_tree.column("Note 1", anchor=tk.E)

        my_tree.insert(parent='', index='end', iid=0, text='Parent', values=("1", "John", "Smith", "5"))
        my_tree.pack()

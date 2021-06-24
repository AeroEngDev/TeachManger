# import own classes
from Student import Student
from Course import Course
from DB_con import *
from Calender import *

import pdb
# import own functions
# from add_course import add_course
#
# from add_grade import add_grade

from Kursinhalt import ManageCourses

# import built functions
import datetime as dt
import tkinter as tk
import tkinter.ttk as ttk
from sqlite3 import *
from init import init
import subprocess
import os


pwd = os.getcwd()

root = tk.Tk()
style = ttk.Style(root)
style.configure("My.TLabel", font=('Arial', 25))
heading_frame = tk.Frame(root)
heading_frame.grid(column=0, row=0)

content_frame = tk.Frame(root)
content_frame.grid(column=0, row=1)

heading_label = ttk.Label(heading_frame, text='Lehrer Tools', style="My.TLabel")
heading_label.grid(column=0, row=0)

# create vertical scrollbar for the treeview widget
tree_scroll = ttk.Scrollbar()

content_frame_for_labels = tk.Frame(content_frame)
content_frame_for_labels.grid(column=0, row=0)

# treeview_messages = ttk.Treeview(content_frame)
# treeview_messages['column'] = ('messages', 'messages2')

# tree_scroll.configure(command=content_frame_for_labels.yview, orient=tk.VERTICAL)

# content_frame_for_labels.configure(yscrollcommand=tree_scroll.set)

# treeview_messages.column("#0", width=10, anchor=tk.W)
# treeview_messages.column("messages", width=1000)
# treeview_messages.column("messages2", width=500)

# treeview_messages.insert('', 'end', text='hallo', values=('Initialisiere Programm...'))
# treeview_messages.grid(column=0, row=0)
tree_scroll.grid(column=1, row=0)
init_obj = init(root, content_frame_for_labels)
# if no databases were found from the system, a new database needs to be created,
# for that the main window needs to wait until the child window, from which the object is
# stored inside of create_database_window, is closed
if init_obj.create_database_window != None:
    root.wait_window(init_obj.create_database_window)
db_connection = init_obj.return_db_connection()
os.chdir(pwd)
msg_start_courses_window = tk.Label(content_frame_for_labels, text='Der Kursbildschirm wird gestartet...')
row_counter = init_obj.get_row_counter()
row_counter += 1
msg_start_courses_window.grid(column=0, row=row_counter)
ManageCourses(db_connection, root)
root.mainloop()

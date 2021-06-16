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
#root.wait_window(init_obj.db_choice_window)
db_connection = init_obj.return_db_connection()
os.chdir(pwd)
msg_start_courses_window = tk.Label(content_frame_for_labels, text='Der Kursbildschirm wird gestartet...')
row_counter = init_obj.get_row_counter()
row_counter += 1
msg_start_courses_window.grid(column=0, row=row_counter)
ManageCourses(db_connection, root)
root.mainloop()
# check if table exists:
# db_connection = DB_con()

# try:
#     #pdb.set_trace()
#     calender_entries_list = db_connection.ShowTable('CalenderEntries')
#
# except sqlite3.OperationalError:
#     db_connection.CreateTableCalenderEntries()
#
# try:
#     students_entries_list = db_connection.ShowTable('Students')
# except sqlite3.OperationalError:
#     db_connection.CreateStudentsTable()
#
# try:
#     courses_entries_list = db_connection.ShowTable('Courses')
# except sqlite3.OperationalError:
#     db_connection.CreateTableAllCourses()
#
# sql = """SELECT AlertTimeing FROM Settings WHERE SelectID = ?"""
# params = (1,)
#
# try:
#     settings_entries_list = db_connection.GetFromDatabase(sql, params)
# except sqlite3.OperationalError:
#     db_connection.CreateTableSettings()
#     # set the default settings
#
#     # default alert timing is 7 days
#     default_AlertTiming = 7  # days
#     sql = f"""INSERT INTO Settings (AlertTiming) VALUES (?)"""
#     params = (default_AlertTiming,)
#     db_connection.addToDatabase(sql, params)
#
#
# # check if Calender Entries are in the current Alert Timeing
# # AlertTiming = settings_entries_list[1]
# # AlertTiming_Dt = dt.timedelta(days=AlertTiming)
# # today_Dt = dt.datetime.today()
# # Date_Until_Check = today_Dt + AlertTiming_Dt
#
# # Create a instance of Calender:
# # Calender_Inst = calender()
# # next_events = Calender_Inst.check_for_alert()
# # Calender_Inst.do_alert()
#
# # def add_course():
# #     add_course.add_course()
#
# # Init the root Widget
#
# welcome_text = tk.Label(root, text='Schulmanager').pack()
# AddCourse_Button = tk.Button(root, text='Kurse verwalten', command=lambda: ManageCourses(db_connection)).pack()
# #AddGrade_Button = Button(root, text='Note hinzufügen', command=add_grade).pack()
# ShowCalender_Button = tk.Button(root, text='Kalender ansehen').pack()
# AddCalenderEntry_Button = tk.Button(root, text='Kalendereintrag hinzufügen').pack()
# ExitApp_Button = tk.Button(root, text='Programm beenden', command=quit).pack()



# print('Hauptmenü\n')
# print('1. Kurs hinzufügen\n')
# print('2. Note eintragen\n')
# print('3. Kalender ansehen\n')
# print('4. Kalendereintrag machen\n')
# print('5. Programm schließen\n')
#
# user_input = input('Auswahl:')
# while user_input != 5:
#     if user_input == 1:
#
#     elif user_input == 2:

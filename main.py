# import own classes
from neuerKurs import *
from DB_con import *
from Calender import *

import pdb
# import own functions
from add_course import add_course
#import add_course as add_course
from add_grade import add_grade

from Kursinhalt import *

# import built functions
import datetime as dt
from tkinter import *
from sqlite3 import *

# check if table exists:
db_connection = DB_con()

try:
    #pdb.set_trace()
    calender_entries_list = db_connection.ShowTable('CalenderEntries')

except sqlite3.OperationalError:
    db_connection.CreateTableCalenderEntries()

try:
    students_entries_list = db_connection.ShowTable('Students')
except sqlite3.OperationalError:
    db_connection.CreateStudentsTable()

try:
    courses_entries_list = db_connection.ShowTable('Courses')
except sqlite3.OperationalError:
    db_connection.CreateTableAllCourses()

sql = """SELECT AlertTimeing FROM Settings WHERE SelectID = ?"""
params = (1,)

try:
    settings_entries_list = db_connection.GetFromDatabase(sql, params)
except sqlite3.OperationalError:
    #pdb.set_trace()
    db_connection.CreateTableSettings()
    # set the default settings

    # default alert timing is 7 days
    default_AlertTiming = 7  # days
    sql = f"""INSERT INTO Settings (AlertTiming) VALUES (?)"""
    params = (default_AlertTiming,)
    db_connection.addToDatabase(sql, params)

    #settings_entries_list.append(default_AlertTiming)

# check if Calender Entries are in the current Alert Timeing
# AlertTiming = settings_entries_list[1]
# AlertTiming_Dt = dt.timedelta(days=AlertTiming)
# today_Dt = dt.datetime.today()
# Date_Until_Check = today_Dt + AlertTiming_Dt

# Create a instance of Calender:
# Calender_Inst = calender()
# next_events = Calender_Inst.check_for_alert()
# Calender_Inst.do_alert()

# def add_course():
#     add_course.add_course()

# Init the root Widget
root = Tk()
#pdb.set_trace()
#call_ManageCourses = lambda db_connection: ManageCourses(db_connection)
#pdb.set_trace()

welcome_text = Label(root, text='Schulmanager').pack()
AddCourse_Button = Button(root, text='Kurse verwalten', command=lambda: ManageCourses( db_connection)).pack()
#AddGrade_Button = Button(root, text='Note hinzufügen', command=add_grade).pack()
ShowCalender_Button = Button(root, text='Kalender ansehen').pack()
AddCalenderEntry_Button = Button(root, text='Kalendereintrag hinzufügen').pack()
ExitApp_Button = Button(root, text='Programm beenden', command=quit).pack()


root.mainloop()
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

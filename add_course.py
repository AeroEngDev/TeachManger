from tkinter import *
from neuerKurs import *


def add_course():

    new_course_window = Toplevel()

    CourseName_Label = Label(new_course_window, text='Kurs Name:')
    CourseName_Entry = Entry(new_course_window)

    CourseName_Label.pack()
    CourseName_Entry.pack()

    CourseYear_Label = Label(new_course_window, text='Kurs Jahrgang:')
    CourseYear_Entry = Label(new_course_window)

    CourseYear_Label.pack()
    CourseYear_Entry.pack()

    ContactPerson_Label = Label(new_course_window, text='Kontakt Person:')
    ContactPerson_Entry = Label(new_course_window)

    ContactPerson_Label.pack()
    ContactPerson_Entry.pack()

    Notes_Label = Label(new_course_window, text='Kurs Jahrgang:')
    Notes_Entry = Label(new_course_window)

    Notes_Label.pack()
    Notes_Entry.pack()

    # Get the Inputs of the Entries
    CourseName = CourseName_Entry.get()
    CourseYear = CourseYear_Entry.get()
    ContactPerson = ContactPerson_Entry.get()
    Notes = Notes_Entry.get()

    newCourse_init = Kurs(CourseName, CourseYear, ContactPerson, Notes)

    new_course_window.mainloop()

import numpy as np
from tkinter import *
import tkinter.messagebox
import re as re

from DB_con import *
from neuerKurs import *

import pdb

class CourseInfo:

    def __init__(self, db_connection, CourseName):
        sql_GET_gradeCount = f"""SELECT GradeStruct.gradeCount
        FROM GradeStruct
        WHERE GradeStruct.CourseID
        IN(SELECT
        Courses.CourseID
        FROM Courses
        WHERE CourseName=?)"""
        params = (CourseName, )
        self.Get_gradeCount = db_connection.GetFromDatabase(sql_GET_gradeCount, params)
        gradeNames_list = []
        gradeWeightNames_list = []
        sql_GET_grades = f"""SELECT
        Students.forename, Students.surname, {CourseName}.grade1,"""
        string_GradeStruct = 'grade1_weight'
        for i in range(2, gradeCount):
            gradeNames_list.append('grade'+str(i))
            gradeWeightNames_list.append('grade'+str(i)+'_weight')
            # Construct Query to get all grades in Course Course_selected
            sql_GET_grades = sql_GET_grades + f""", {Course_selected}.grade{i}"""
            # Construct String for GradeStruct
            string_GradeStruct = string_GradeStruct+f", grade{i}_weight"

        sql_GET_grades = sql_GET_grades+f""" FROM {Course_selected} INNER JOINS {Course_selected} ON students.id = {Course_selected}.StudentID """

        self.Selected_Course_NamesGrades_list = db_connection.GetFromDatabase(sql_GET_grades, ())

        #  Get the Grade Structure
        sql_GET_gradeStruct = f"""SELECT {string_GradeStruct}
        FROM GradeStruct
        WHERE CourseID
        IN (
        SELECT Courses.CourseID
        FROM Courses
        WHERE Courses.CourseName = {Course_selected})"""

        GET_GradeStruct = db_connection.GetFromDatabase(sql_GET_gradeStruct, ())

        self.db_connection = db_connection

    def build_grid(self):

        rows = len(self.Selected_Course_NamesGrades_list)
        columns = len(self.Selected_Course_NamesGrades_list[0])
        entryWidget_list = np.empty(rows, columns)
        edited_text = np.empty(rows, columns)
        Label_forname = Label(root, text='Vorname').grid(row=0, column=0)
        Label_surname = Label(root, text='Nachname').grid(row=0, column=1)

        sql_GET_gradeNames = f"""SELECT grade1_Name"""
        for i in range(2, self.Get_gradeCount):
            sql_GET_gradeNames = sql_GET_gradeNames+f""",grade{i}_Name"""

        sql_GET_gradeNames = sql_GET_gradeNames + f""" FROM GradeNames WHERE GradeNames.CourseID IN(SELECT Courses.CourseID FROM Courses WHERE CourseName =?)"""
        params = (CourseName, )

        gradeNames = self.db_connection.GetFromDatabase(sql_GET_gradeNames, params)

        for i, gradeName in enumerate(gradeNames):
            Label(root, text=gradeName).grid(row=0, column=2+i)

        for i, set in enumerate(self.Selected_Course_NamesGrades_list):
            for j, entry in enumerate(set):
                #entry_widget_list[i, j]
                edited_text[i, j] = VarString()
                edited_text[i, j].set(str(entry))
                entryWidget_list[i, j] = Entry(root, textvariable=edited_entries[i ,j]).grid(row=i+1, column=j)

class CoursesDropdown_menu:

    def __init__(self, db_connection, root):
        self.root = root
        sql = f"""SELECT CourseID, CourseName FROM Courses"""
        #pdb.set_trace()
        Courses_list = db_connection.GetFromDatabase(sql, ())
        CourseString_list = []
        for Course_Tupel in Courses_list:
            CourseString_list.append(f"{Course_Tupel[0]}, {Course_Tupel[1]}")

        CourseString_list.append('Neuer Kurs')
        # Create Dropdown-Widget with the CorseNames
        clicked = StringVar()
        clicked.set(CourseString_list[0])
        widget_dropdown_CourseNames = OptionMenu(self.root, clicked, *CourseString_list)
        widget_dropdown_CourseNames.pack()
        widget_dropdown_CourseNames.bind("<ButtonRelease-1>",lambda event: self.InspectDropdownValue(event))
        self.CourseIDName = clicked.get()

        self.NewCourse_Widgets = ButtonsNewCourseEntry(self.root, db_connection)
        self.db_connection = db_connection

    def InspectDropdownValue(self, event):
        if self.CourseIDName != 'Neuer Kurs':
            # if the Buttons for new Course are shown, hide them:
            if self.NewCourse_Widgets.Check() is True:
                self.NewCourse_Widgets.Hide()
            #pdb.set_trace()
            # Get CourseID:
            CourseID_pos = self.CourseIDName.find(',')
            CourseID = self.CourseIDName[0:CourseID_pos]

            sql_get_courseInfo = f"""SELECT * FROM Courses WHERE CourseID = ?"""
            params = (CourseID,)
            Get_CourseInfo = self.db_connection.GetFromDatabase(sql_get_courseInfo, params)
            pdb.set_trace()
            self.SelectedCourse = Course(self.db_connection, Get_CourseInfo[1], Get_CourseInfo[2], Get_CourseInfo[3], Get_CourseInfo[4], Get_CourseInfo[0])
            courseInfo = CourseInfo(self.db_connection, self.CourseName)
            widget_list = self.root.slaves()
        else:

            if self.NewCourse_Widgets.Check() is True:
                pass
            else:
                self.NewCourse_Widgets.Show()



class ButtonsNewCourseEntry:

    def __init__(self, root, db_connection):

        self.root = root
        self.db_connection = db_connection

        self.NewCourseName = StringVar()
        self.NewCourseName.set('Kursname')
        self.Entry_CourseName = Entry(self.root, textvariable=self.NewCourseName)

        self.NewCourseYear = StringVar()
        self.NewCourseYear.set('Jahrgang')
        self.Entry_CourseYear = Entry(self.root, textvariable=self.NewCourseYear)

        self.NewCourseContact = StringVar()
        self.NewCourseContact.set('Kontaktperson')
        self.Entry_CourseContact = Entry(self.root, textvariable=self.NewCourseContact)

        self.NewCourseNotes = StringVar()
        self.NewCourseNotes.set('Notizen')
        self.Entry_CourseNotes = Entry(self.root, textvariable=self.NewCourseNotes)

        self.SubmitButton = Button(self.root, text='Erstellen', command=self.SubmitNewCourse)



    def Show(self):

        self.Entry_CourseName.pack()
        self.Entry_CourseYear.pack()
        self.Entry_CourseContact.pack()
        self.Entry_CourseNotes.pack()
        self.SubmitButton.pack()

    def Hide(self):

        self.Entry_CourseName.pack_forget()
        self.Entry_CourseYear.pack_forget()
        self.Entry_CourseNotes.pack_forget()
        self.Entry_CourseContact.pack_forget()
        self.SubmitButton.pack_forget()

    def Check(self):
        ## only check for one Entry Field:
        return self.Entry_CourseName.winfo_ismapped()

    def SubmitNewCourse(self):

        CourseName = self.NewCourseName.get()
        Year = self.NewCourseYear.get()
        Contact = self.NewCourseContact.get()
        Notes = self.NewCourseNotes.get()
        msg = f"""Soll der Kurs so eingetragen werden?
        \n Kursname: {CourseName}
        \n Jahrgang: {Year}
        \n Ansprechpartner: {Contact}
        \n Notizen: {Notes}"""
        user_return = tkinter.messagebox.askyesno(title='Kurs eintragen?', message=msg)
        #pdb.set_trace()
        if user_return == True:
            # set CourseId -1 if its a new Course
            self.SelectedCourse = Course(self.db_connection, CourseName, Year, Contact, Notes, -1)

        self.Hide()

        Label(self.root, text=f"Möchtest Du Schüler zum Kurs {self.NewCourseName} hinzufügen?").pack()

        ## Create an Instance of AddParticipant
        #self.participant_window =
        ## work on this again!!

        Button(self.root, text=f"Teilnehmende hinzufügen", command=lambda: AddParticipant(self.db_connection)).pack()
        Button(self.root, text="Zurück zum Hauptmenü", command=self.root.Destroy)

class AddParticipant:

    def __init__(self, db_connection):

        self.db_connection = db_connection
        self.AddParticipant_window = Toplevel()
        Label(self.AddParticipant_window, text="Es können Teilnehmende, die schon in der Datenbank sind, in den Kurs eingetragen werden, oder neue Teilnehmende in das System aufgenommenw werden.").pack()

        sql_GET_participants = "SELECT Students.id, Students.forname, Students.surname FROM Students"
        participants_list = self.db_connection.GetFromDatabase(sql_GET_participants, ())
        part_string_list = []
        for partTupel in participants_list:
            part_string_list.append(f"{partTupel[0]}, {partTupel[1]}, {partTupel[2]}")
        part_string_list.insert(0, 'Teilnehmenden hinzufügen')
        self.participant_shown = StringVar()
        self.participant_shown.set(part_string_list[0])
        widget_dropdown_Participants = OptionMenu(self.AddParticipant_window, self.participant_shown, *part_string_list).pack()
        widget_dropdown_Participants.bind("<ButtonRelease-1>",lambda event: self.InspectParticipantsDropDown(event))

        self.NewPartForname = StringVar()
        self.NewPartForname = self.NewPartForname.set('Vorname')
        self.FornamePartEntry = Entry(self.AddParticipant_window, textvariable=self.NewPartForname)

        self.NewPartSurname = StringVar()
        self.NewPartSurname = self.NewPartSurname.set('Nachname')
        self.SurnamePartEntry = Entry(self.AddParticipant_window, textvariable=self.NewPartSurname)

        self.NewPartYear = StringVar()
        self.NewPartYear = self.NewPartYear.set('Jahrgang')
        self.YearPartEntry = Entry(self.AddParticipant_window, textvariable=self.NewPartYear)

        self.NewPartTutor = StringVar()
        self.NewPartTutor = self.NewPartTutor.set('Tutor')
        self.TutorPartEntry = Entry(self.AddParticipant_window, textvariable=self.NewPartTutor)

        self.SubmitNewParticipant = Button(self.AddParticipant_window, text='Eintragen', command=self.InspectNewParticipant_Entries)



    def Show_Widgets(self):
        self.FornamePartEntry.pack()
        self.SurnamePartEntry.pack()
        self.YearPartEntry.pack()
        self.TutorPartEntry.pack()
        self.SubmitNewParticipant.pack()

    def Hide_Widgets(self):
        self.FornamePartEntry.pack_forget()
        self.SurnamePartEntry.pack_forget()
        self.YearPartEntry.pack_forget()
        self.TutorPartEntry.pack_forget()
        self.SubmitNewParticipant.pack_forget()

    def Check_Widgets(self):
        return self.FornamePartEntry.winfo_ismapped()

    def InspectNewParticipant_Entries(self):

        msg = f"""Soll der Kurs so eingetragen werden?
        \n Name: {self.FornamePartEntry.get()} {self.SurnamePartEntry.get()}
        \n Klassenstufe: {self.YearPartEntry.get()}
        \n Tutor: {self.TutorPartEntry.get()}"""
        user_return = tkinter.messagebox.askyesno(title='Teilnehmer erstellen & eintragen?', message=msg)
        if user_return is True:
            self.AddedStudent = Student(self.NewPartForname, self.NewPartSurname, self.NewPartYear, self.NewPartTutor)
            self.SelectedCourse.AddStudent(self.AddedStudent.Get_ID())

    def InspectParticipantsDropDown(self):

        if self.participant_shown.get() == 'Teilnehmenden hinzufügen':
            if Check_Widgets is False:
                self.Show_Widgets()
        else:
            if Check_Widgets is True:
                self.Hide_Widgets()
            # If a already existent participant is selected, he gets add to the Course
            # Decompose String to Tupel
            dec_string = self.participant_shown
            selection = dec_string[0:dec_string.find(',')]




def ManageCourses(db_connection):

    root = Toplevel()
    DropDownMenu = CoursesDropdown_menu(db_connection, root)

    root.mainloop()

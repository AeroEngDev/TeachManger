import numpy as np
import tkinter as tk
import tkinter.messagebox
import re as re

from DB_con import *
from neuerKurs import *
from PieChart import *

import pdb


class CourseInfo:

    def __init__(self, db_connection, SelectedCourse_obj, root):
        self.db_connection = db_connection
        self.Frame_Obj = root
        self.root = root[1]
        self.PieFrame = root[2]
        self.MaintanceFrame = root[3]
        self.CourseName = SelectedCourse_obj.Get_CourseName()
        self.SelectedCourse_obj = SelectedCourse_obj

        # Get the Infos about this course ouf of the db
        self.GET_CourseInfo()

        # Initalise The Pie Chart:
        self.PieChart_obj = PieChart(self.PieFrame, self.db_connection, self.SelectedCourse_obj, self)
        self.PieChart_obj.init_event_handlers()

        MaintainCourses_Menu(self.Frame_Obj, db_connection, self.SelectedCourse_obj, self.edited_text, self.entryWidget_list, self)

    def GET_CourseInfo(self):

        # Inner Join, get student_id and Student Names
        sql_get_course_content = "SELECT stud_courses.student_id, Students.forname, Students.surname FROM stud_courses INNER JOIN Students ON Students.student_id = stud_courses.student_id WHERE stud_courses.course_id = ?"
        student_ids_in_course = self.db_connection.GetFromDatabase(sql_get_course_content, (self.SelectedCourse_obj.Get_CourseID(),))
        student_ids_in_course = list(dict.fromkeys(student_ids_in_course))

        # get the grades out of the junktion table
        grades_of_students_in_course = []
        for student in student_ids_in_course:
            sql_get_grades_for_id = "SELECT stud_courses_grades.grade_id, grade_value, grade_name, grade_weight  FROM stud_courses_grades INNER JOIN Grades ON Grades.grade_id = stud_courses_grades.grade_id WHERE student_id = ?"
            grades_for_student_id = self.db_connection.GetFromDatabase(sql_get_grades_for_id, (student[0],))
            if grades_for_student_id != []:
                grades_of_students_in_course.append(grades_for_student_id[0])
        # get the weights and the grade names
        grade_names = {}
        grade_weights = {}
        sql_get_weight_names = "SELECT grade_id, grade_name, grade_weight FROM Grades WHERE course_id = ?"
        grade_info_course = self.db_connection.GetFromDatabase(sql_get_weight_names, (self.SelectedCourse_obj.Get_CourseID(),))
        for row in grade_info_course:
            grade_names[row[0]] = row[1]
            grade_weights[row[0]] = row[2]

        self.student_ids_in_course = student_ids_in_course
        self.grades_of_students_in_course = grades_of_students_in_course
        self.grade_names = grade_names
        self.grade_weights = grade_weights
        # build the grid of entries
        self.edited_text, self.entryWidget_list = self.build_grid()

    def Clear_Frame(self):
        # remove widgets in CourseInfor Frame
        for Widget in self.root.winfo_children():
            Widget.destroy()
        # remove widgets in Pie Frame
        for Widget in self.PieFrame.winfo_children():
            Widget.destroy()

    def Clear_CourseInfo(self):
        # remove widgets in CourseInfor Frame
        for Widget in self.root.winfo_children():
            Widget.destroy()

    def Get_Vars(self):
        return self.column_desc_list, self.edited_text

    def build_grid(self):

        try:
            columns = len(self.grades_of_students_in_course[0])
        except:
            columns = 0
        # extra_entry = []
        # for i in range(0, columns):
        #     extra_entry.append('')
        # extra_entry = (extra_entry)
        # self.Selected_Course_NamesGrades_list.append(extra_entry)

        sql_get_grade_info = "SELECT grade_id, grade_name, grade_weight FROM Grades WHERE course_id = ?"
        get_grade_info = self.db_connection.GetFromDatabase(sql_get_grade_info, (self.SelectedCourse_obj.Get_CourseID(),))

        #rows = len(self.grades_of_students_in_course)

        #pdb.set_trace()
        self.entryWidget_list = []
        self.edited_text = []
        self.column_desc_list = []
        self.column_desc_list.append(tk.Label(self.root, text='Student ID'))
        self.column_desc_list[0].grid(row=0, column=0)
        self.column_desc_list.append(tk.Label(self.root, text='Vorname'))
        #Label_forname = Label(self.root, text='Vorname')
        self.column_desc_list[1].grid(row=0, column=1)
        self.column_desc_list.append(tk.Label(self.root, text='Nachname'))
        self.column_desc_list[2].grid(row=0, column=2)

        i = 1
        for grade_id, grade_name in self.grade_names.items():
            self.column_desc_list.append(tk.Label(self.root, text=f"{grade_id}, {grade_name}"))

            self.column_desc_list[2+i].grid(row=0, column=2+i)
            #if grade_id in

            i = i+1

        self.entryWidget_list = []
        self.edited_text = []
        for i, student in enumerate(self.student_ids_in_course):

            self.edited_text_set = []
            self.entryWidget_list_set = []
            # Build the label field for the student id
            self.edited_text_set.append(tk.StringVar())
            self.edited_text_set[0].set(student[0])
            self.entryWidget_list_set.append(tk.Label(self.root, text=self.edited_text_set[0].get()))
            self.entryWidget_list_set[0].grid(column=0, row=i+1)

            # build the entry field for the forname
            self.edited_text_set.append(tk.StringVar())
            self.edited_text_set[1].set(student[1])
            self.entryWidget_list_set.append(tk.Entry(self.root, textvariable=self.edited_text_set[1]))
            self.entryWidget_list_set[1].grid(column=1, row=i+1)

            # build the entry field for the surname
            self.edited_text_set.append(tk.StringVar())
            self.edited_text_set[2].set(student[2])
            self.entryWidget_list_set.append(tk.Entry(self.root, textvariable=self.edited_text_set[2]))
            self.entryWidget_list_set[2].grid(column=2, row=i+1)
            j = 1
            #pdb.set_trace()
            for grade_id, grade_name in self.grade_names.items():
                self.edited_text_set.append(tk.StringVar())
                # insert grade for the grade_id
                #pdb.set_trace()

                for tuple in self.grades_of_students_in_course:
                    #pdb.set_trace()
                    if tuple[0] == grade_id:
                        self.edited_text_set[len(self.edited_text_set)-1].set(tuple[1])
                self.entryWidget_list_set.append(tk.Entry(self.root, textvariable=self.edited_text_set[len(self.edited_text_set)-1]))
                self.entryWidget_list_set[len(self.entryWidget_list_set)-1].grid(column=2+j, row=i+1)
                j = j + 1
            self.edited_text.append(self.edited_text_set)
            self.entryWidget_list.append(self.entryWidget_list_set)
        return self.edited_text, self.entryWidget_list

    def Update(self):
        msg = """Bist du sicher, dass du die Änderungen so in die Datenbank schreiben möchtest? Alle Daten werden so in die Datenbank geschrieben!"""
        user_return = tkinter.messagebox.askyesno(title='Änderungen speichern?', message=msg)
        if user_return is True:
            number_of_rows = len(self.edited_text)
            number_of_columns = len(self.edited_text[0])
            # a dataset is a whole row of the table, while a entry is just one entry of the table
            data_students = []
            data_grades = []
            for dataset in self.edited_text:
                dataset_students_list = []
                dataset_grades_list = []
                for i, entry in enumerate(dataset):

                    if i == 0:
                        student_id = entry.get()
                    elif i == 1 or i == 2:
                        pass
                    else:
                        desc_of_column = self.column_desc_list[i].cget('text')
                        pos_of_komma = desc_of_column.find(',')
                        grade_id = desc_of_column[0:pos_of_komma]

                        # check if there is already an entry for the grade id in the db
                        sql_check_if_grade_id_in_stud_courses_grades = "SELECT grade_value FROM stud_courses_grades WHERE grade_id = ?"
                        grade_value_for_grade_id = self.db_connection.GetFromDatabase(sql_check_if_grade_id_in_stud_courses_grades, (grade_id, ))

                        course_id = self.SelectedCourse_obj.Get_CourseID()
                        # get grade_value
                        if dataset[i].get() != '':
                            grade_value = int(dataset[i].get())
                        else:
                            grade_value = ''
                        if type(grade_value) == int:

                            if grade_value_for_grade_id != []:
                                if grade_value_for_grade_id[0][0] != grade_value:
                                    sql_update_grade_value_for_grade_id = f"""UPDATE stud_courses_grades SET
                                    student_id = {student_id},
                                    course_id = {self.SelectedCourse_obj.Get_CourseID()},
                                    grade_id = {grade_id},
                                    grade_value = {grade_value}
                                    WHERE
                                    student_id = ?,
                                    course_id = ?,
                                    grade_id = ?,
                                    grade_value = ?
                                    """
                                    params = (student_id, course_id, grade_id, grade_value_for_grade_id[0][0])
                                    self.db_connection.addToDatabase(sql_update_grade_value_for_grade_id, params)
                            else:
                                sql_insert_into_stud_courses_grades = "INSERT INTO stud_courses_grades (student_id, course_id, grade_id, grade_value) VALUES (?, ?, ?, ?)"
                                params = (student_id, course_id, grade_id, grade_value)
                                self.db_connection.addToDatabase(sql_insert_into_stud_courses_grades, params)

        def __del__(self):
            for row in self.entryWidget_list:
                for widget in row:
                    widget.destroy()


class MaintainCourses_Menu(CourseInfo):

    def __init__(self, root, db_connection, SelectedCourse_obj, text_obj_of_entries, widget_objects_of_entries, courseInfo_obj):
        self.Frame_Obj = root
        self.root = root[3]
        self.db_connection = db_connection
        self. SelectedCourse_obj = SelectedCourse_obj

        self.courseInfo_obj = courseInfo_obj

        self.edited_text = text_obj_of_entries
        self.entryWidget_list = widget_objects_of_entries
        #self.CourseName = SelectedCourse_obj.GET_CourseName()

        self.Update_Course_Table = tk.Button(self.root, text='Änderungen Speichern', command=self.Start_Update)
        self.Update_Course_Table.grid(column=0, row=0)
        #AddParticipant_BE = AddParticipant(db_connection, CourseName)
        self.AddNewParticipants = tk.Button(self.root, text='Teilnehmende hinzufügen', command=self.Start_AddPart)
        self.AddNewParticipants.grid(column=1, row=0)

        self.CourseName = SelectedCourse_obj.Get_CourseName()

    def Start_AddPart(self):
        add_part = AddParticipant(self.db_connection, self.SelectedCourse_obj)

    def Start_Update(self):
        self.root = self.Frame_Obj[1]

        self.column_desc_list, self.edited_text = self.courseInfo_obj.Get_Vars()
        self.Update()


class CoursesDropdown_menu:

    def __init__(self, db_connection, Framelist):

        DropdownMenuFrame = Framelist[0]
        CourseInfoFrame = Framelist[1]
        PieFrame = Framelist[2]
        AddParticipantFrame = Framelist[3]
        self.FrameList = [DropdownMenuFrame, CourseInfoFrame, PieFrame, AddParticipantFrame]
        self.courseInfo = None
        self.CourseObj = None
        self.widget_dropdown_CourseNames = None
        self.db_connection = db_connection
        self.DropdownMenuFrame = DropdownMenuFrame

        self.courses_des_label = tk.Label(DropdownMenuFrame, text='Kurs auswählen:')

        # Initalise Widgets, which show Information about the selectede Course:
        msg = "Gespeicherte Informationen über den Kurs:"
        self.Description_Label = tk.Label(DropdownMenuFrame, text=msg)

        self.CourseID_Description_Label = tk.Label(DropdownMenuFrame, text='Kurs ID')
        self.CourseID_Label_Text = tk.StringVar()
        self.CourseID_Label = tk.Label(DropdownMenuFrame, text=self.CourseID_Label_Text.get())

        self.CourseName_Description_Label = tk.Label(DropdownMenuFrame, text='Kursname:')
        self.CourseName_Entry_Text = tk.StringVar()
        self.CourseName_Entry = tk.Entry(DropdownMenuFrame, textvariable=self.CourseName_Entry_Text)

        self.Course_Year_Description_Label = tk.Label(DropdownMenuFrame, text='Klassenstufe')
        self.Course_Year_Text = tk.StringVar()
        self.Course_Year_Entry = tk.Entry(DropdownMenuFrame, textvariable=self.Course_Year_Text)

        self.ContactName_Description_Label = tk.Label(DropdownMenuFrame, text='Ansprechpartner:')
        self.ContactName_Text = tk.StringVar()
        self.ContactName_Entry = tk.Entry(DropdownMenuFrame, textvariable=self.ContactName_Text)

        self.Course_Notes_Description_Label = tk.Label(DropdownMenuFrame, text='Notizen:')
        self.Course_Notes_Text = tk.StringVar()
        self.Course_Notes_Entry = tk.Entry(DropdownMenuFrame, textvariable=self.Course_Notes_Text)

        self.Course_submit_changes = tk.Button(DropdownMenuFrame, text='Änderungen speichern', command=self.Submit_Course_Changes)


        # Widgets to Insert a new Course
        self.NewCourseName = tk.StringVar()
        self.NewCourseName.set('Kursname')
        self.Entry_CourseName = tk.Entry(DropdownMenuFrame, textvariable=self.NewCourseName)

        self.NewCourseYear = tk.StringVar()
        self.NewCourseYear.set('Jahrgang')
        self.Entry_CourseYear = tk.Entry(DropdownMenuFrame, textvariable=self.NewCourseYear)

        self.NewCourseContact = tk.StringVar()
        self.NewCourseContact.set('Kontaktperson')
        self.Entry_CourseContact = tk.Entry(DropdownMenuFrame, textvariable=self.NewCourseContact)

        self.NewCourseNotes = tk.StringVar()
        self.NewCourseNotes.set('Notizen')
        self.Entry_CourseNotes = tk.Entry(DropdownMenuFrame, textvariable=self.NewCourseNotes)

        self.SubmitButton = tk.Button(DropdownMenuFrame, text='Erstellen', command=self.SubmitNewCourse)

        # save the new course widgets in a list
        self.NewCourseWidgets = [self.Entry_CourseName, self.Entry_CourseYear, self.Entry_CourseContact, self.Entry_CourseNotes, self.SubmitButton]


        #self.root = DropdownMenuFrame
        self.CourseInfoFrame = CourseInfoFrame

        self.refresh_widgets()

        # create a button to delete course
        self.delete_course_button = tk.Button(DropdownMenuFrame, text='Kurs löschen', command=self.delete_course)


        self.CourseIDName = self.clicked.get()


    def refresh_widgets(self):
        # if the widget already exists, delete it
        if self.widget_dropdown_CourseNames is not None:
            self.widget_dropdown_CourseNames.destroy()
        # load all courses out of courses table
        self.load_courses_from_db()
        # Create Dropdown-Widget with the CorseNames
        self.clicked = tk.StringVar()
        self.clicked.set(self.CourseString_list[0])
        self.widget_dropdown_CourseNames = tk.OptionMenu(self.DropdownMenuFrame, self.clicked, *self.CourseString_list)
        self.widget_dropdown_CourseNames.grid(column=1, row=0)
        self.clicked.trace("w", self.InspectDropdownValue)
        #self.widget_dropdown_CourseNames.bind("<ButtonRelease-1>", lambda event: self.InspectDropdownValue(event))

    def delete_course(self):
        msg = f"Bist du sicher, dass du den Kurs {self.clicked.get()} löschen möchtest?"
        user_return = tkinter.messagebox.askyesno(title='Kurs löschen?', message=msg)
        if user_return is True:
            sql_delete_course = "DELETE FROM Courses WHERE course_id = ?"
            self.db_connection.addToDatabase(sql_delete_course, (self.CourseObj.Get_CourseID(),))
            self.refresh_widgets()

    def load_courses_from_db(self):
        sql = """SELECT course_id, course_name FROM Courses"""
        Courses_list = self.db_connection.GetFromDatabase(sql, ())

        CourseString_list = []
        for Course_Tupel in Courses_list:
            CourseString_list.append(f"{Course_Tupel[0]}, {Course_Tupel[1]}")

        CourseString_list.append('Neuer Kurs')
        self.CourseString_list = CourseString_list

    def Submit_Course_Changes(self):
        msg = f"""Sollen die Änderungen wirklich in die Datenbank geschrieben werden?"""
        user_return = tkinter.messagebox.askyesno(title='Kurs eintragen?', message=msg)
        if user_return is True:
            params = (self.CourseName_Entry_Text.get(), self.Course_Year_Text.get(), self.ContactName_Text.get(), self.Course_Notes_Text.get())
            sql = f"UPDATE Courses SET course_name = ?, year = ?, contact_name = ?, notes = ? WHERE course_id ={self.CourseID_Label_Text.get()}"
            self.db_connection.addToDatabase(sql, params)

    def Show(self):
        # update the value of the courseID label field:
        self.CourseID_Label = tk.Label(self.DropdownMenuFrame, text=self.CourseID_Label_Text.get())

        if self.CourseID_Label.winfo_ismapped() == 0:
            # delete course button widget
            self.delete_course_button.grid(column=2, row=0)

            self.courses_des_label.grid(column=0, row=0)

            self.Description_Label.grid(column=0, row=1)
            self.CourseID_Description_Label.grid(column=1, row=1)
            self.CourseID_Label.grid(column=1, row=2)

            self.CourseName_Description_Label.grid(column=2, row=1)
            self.CourseName_Entry.grid(column=2, row=2)

            self.Course_Year_Description_Label.grid(column=3, row=1)
            self.Course_Year_Entry.grid(column=3, row=2)

            self.ContactName_Description_Label.grid(column=4, row=1)
            self.ContactName_Entry.grid(column=4, row=2)

            self.Course_Notes_Description_Label.grid(column=5, row=1)
            self.Course_Notes_Entry.grid(column=5, row=2)

            self.Course_submit_changes.grid(column=2, row=3)

    def Hide(self):

        self.Description_Label.grid_forget()
        self.CourseID_Description_Label.grid_forget()
        self.CourseName_Description_Label.grid_forget()
        self.Course_Year_Description_Label.grid_forget()
        self.ContactName_Description_Label.grid_forget()
        self.Course_Notes_Description_Label.grid_forget()

        self.CourseID_Label.grid_forget()
        self.CourseName_Entry.grid_forget()
        self.Course_Year_Entry.grid_forget()
        self.ContactName_Entry.grid_forget()
        self.Course_Notes_Entry.grid_forget()

        # delete course button
        self.delete_course_button.grid_forget()

        self.Course_submit_changes.grid_forget()

    def InspectDropdownValue(self, *args):

        if self.courseInfo is not None:
            self.courseInfo.Clear_Frame()

        if self.clicked.get() != 'Neuer Kurs':
            if self.Check_Buttons_New_Course() == 1:
                for Widget in self.NewCourseWidgets:
                    Widget.destroy()
            self.CourseIDName = self.clicked.get()
            # Get CourseID:
            CourseID_pos = self.CourseIDName.find(',')
            CourseID = self.CourseIDName[0:CourseID_pos]

            sql_get_courseInfo = """SELECT * FROM Courses WHERE course_id = ?"""
            params = (CourseID,)
            Get_CourseInfo = self.db_connection.GetFromDatabase(sql_get_courseInfo, params)
            Get_CourseInfo = Get_CourseInfo[0]
            self.CourseID_Label_Text.set(CourseID)
            self.CourseName_Entry_Text.set(Get_CourseInfo[1])
            self.Course_Year_Text.set(Get_CourseInfo[2])
            self.ContactName_Text.set(Get_CourseInfo[3])
            self.Course_Notes_Text.set(Get_CourseInfo[4])
            self.Show()
            self.CourseObj = Course(self.db_connection, Get_CourseInfo[1], Get_CourseInfo[2], Get_CourseInfo[3], Get_CourseInfo[4], Get_CourseInfo[0])

            self.courseInfo = CourseInfo(self.db_connection, self.CourseObj, self.FrameList)
        else:
            # if we set the dropdown menu to New Course, the CourseObj is set to None
            # to make sure that not the wrong course is edited
            self.CourseObj = None



            self.Hide()
            self.Show_Buttons_New_course()
            if self.Check_Buttons_New_Course() is True:
                pass
            else:
                self.Show_Buttons_New_course()

    def GET_Course_Obj(self):
        return self.CourseObj

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
        if user_return is True:
            # set CourseId -1 if its a new Course
            self.SelectedCourse = Course(self.db_connection, CourseName, Year, Contact, Notes, -1)
        #self.Hide()

        # set the values in the entry fields for the edit of the course info with the data
        # of the new course
        self.CourseName_Entry_Text.set(CourseName)
        self.Course_Year_Text.set(Year)
        self.ContactName_Text.set(Contact)
        self.Course_Notes_Text.set(Notes)
        # load the course list so that the new course appears in the dropdown menu
        self.refresh_widgets()
        self.Hide_Buttons_New_Course()
        self.Show()
        CourseInfo(self.db_connection, self.SelectedCourse, self.FrameList)

    def Show_Buttons_New_course(self):

        self.Entry_CourseName.grid(column=0, row=1)
        self.Entry_CourseYear.grid(column=0, row=2)
        self.Entry_CourseContact.grid(column=0, row=3)
        self.Entry_CourseNotes.grid(column=0, row=4)
        self.SubmitButton.grid(column=0, row=5)

    def Hide_Buttons_New_Course(self):

        self.Entry_CourseName.grid_forget()
        self.Entry_CourseYear.grid_forget()
        self.Entry_CourseNotes.grid_forget()
        self.Entry_CourseContact.grid_forget()
        self.SubmitButton.grid_forget()

    def Check_Buttons_New_Course(self):
        # only check for one Entry Field:
        return self.Entry_CourseName.winfo_ismapped()


class AddParticipant(CourseInfo):

    def __init__(self, db_connection, SelectedCourse_obj):

        self.SelectedCourse_obj = SelectedCourse_obj

        self.db_connection = db_connection
        self.AddParticipant_window = tk.Toplevel()

        # get all students
        #get all students who are in the selected course
        self.check_students_in_course()
        self.build_grid()

    def check_students_in_course(self):
        sql_GET_students_info = "SELECT * FROM Students"
        self.students_info = self.db_connection.GetFromDatabase(sql_GET_students_info, ())

        sql_students_in_selected_course = "SELECT student_id FROM stud_courses WHERE course_id = ?"
        self.students_in_selected_course = self.db_connection.GetFromDatabase(sql_students_in_selected_course, (self.SelectedCourse_obj.Get_CourseID(),))
        list = []
        for student_id in self.students_in_selected_course:
            list.append(student_id[0])
        self.students_in_selected_course = list

    def build_grid(self):

        start_column = 0
        start_row = 0
        try:
            columns = len(self.students_info[0])
        except:
            columns = 0
        rows = len(self.students_info)

        # build first row:
        self.student_id_label = tk.Label(self.AddParticipant_window, text='Student ID')
        self.student_forname_label = tk.Label(self.AddParticipant_window, text='Vorname')
        self.student_surname_label = tk.Label(self.AddParticipant_window, text='Nachname')
        self.student_year_label = tk.Label(self.AddParticipant_window, text='Klasse')
        self.student_tutor_label = tk.Label(self.AddParticipant_window, text='Tutor')
        self.add_to_course_box = tk.Label(self.AddParticipant_window, text='Zu Kurs hinzufügen?')

        self.student_id_label.grid(column=start_column, row=start_row)
        self.student_forname_label.grid(column=start_column+1, row=start_row)
        self.student_surname_label.grid(column=start_column+2, row=start_row)
        self.student_year_label.grid(column=start_column+3, row=start_row)
        self.student_tutor_label.grid(column=start_column+4, row=start_row)

        Widgets_entry_list = []
        Widgets_label_id_list = []
        entry_var = []
        entry_list = []
        checkbox_list = []
        checkbox_var_list = []
        widget_list_row = []
        for current_row_number in range(0, rows):
            current_row = self.students_info[current_row_number]
            if current_row[0] in self.students_in_selected_course:
                bgcolor = 'yellow'
            else:
                bgcolor = 'white'

            widget_list_row.append(tk.Label(self.AddParticipant_window, text=current_row[0], bg=bgcolor))
            widget_list_row[current_row_number].grid(column=start_column, row=start_row+current_row_number+1)
            entry_list_row = []
            entry_var_row = []
            for current_column_number in range(0, len(current_row)-1):

                aktuell = tk.StringVar()
                aktuell.set(current_row[current_column_number+1])
                entry_var_row.append(aktuell)
                entry_list_row.append(tk.Entry(self.AddParticipant_window, textvariable=entry_var_row[current_column_number], bg=bgcolor))
                entry_list_row[current_column_number].grid(column=start_column+current_column_number+1, row=start_row+current_row_number+1)
            checkbox_value = tk.StringVar()
            checkbox_value.set('0')
            checkbox_var_list.append(checkbox_value)

            checkbox_list.append(tk.Checkbutton(self.AddParticipant_window, variable=checkbox_var_list[len(checkbox_var_list)-1], onvalue=1, offvalue=0, text='Zu Kurs hinzufügen?'))
            pdb.set_trace()
            if current_row[0] in self.students_in_selected_course:
                checkbox_list[len(checkbox_list)-1].config(state=DISABLED)
                checkbox_var_list[len(checkbox_var_list)-1].set('0')

            checkbox_list[len(checkbox_list)-1].grid(column=start_column+current_column_number+2, row=start_row+current_row_number+1)


            entry_list.append(entry_list_row)
            entry_var.append(entry_var_row)
        self.add_new_student_to_system = tk.StringVar()
        self.add_new_student_to_system.set('0')
        self.Checkbox_Add_new_student_to_system = tk.Checkbutton(self.AddParticipant_window, text='Neuen Teilnehmenden hinzufügen', onvalue=1, offvalue=0, variable=self.add_new_student_to_system, command=self.show_new_student_widgets)
        self.Checkbox_Add_new_student_to_system.grid(column=start_column, row=len(self.students_info)+2)

        self.new_stud_widget_list = []
        self.new_stud_var_list = []

        # New Field for Forname
        self.new_stud_var_list.append(tk.StringVar())
        self.new_stud_var_list[0].set('Vorname')
        self.new_stud_widget_list.append(tk.Entry(self.AddParticipant_window, textvariable=self.new_stud_var_list[0]))
        # New Field for Surname
        self.new_stud_var_list.append(tk.StringVar())
        self.new_stud_var_list[1].set('Nachname')
        self.new_stud_widget_list.append(tk.Entry(self.AddParticipant_window, textvariable=self.new_stud_var_list[1]))
        # New Field for School Year
        self.new_stud_var_list.append(tk.StringVar())
        self.new_stud_var_list[2].set('Schuljahr')
        self.new_stud_widget_list.append(tk.Entry(self.AddParticipant_window, textvariable=self.new_stud_var_list[2]))
        # new Field for Tutor
        self.new_stud_var_list.append(tk.StringVar())
        self.new_stud_var_list[3].set('Tutor')
        self.new_stud_widget_list.append(tk.Entry(self.AddParticipant_window, textvariable=self.new_stud_var_list[3]))

        # show it on screen

        checkbox_var_list.append(tk.StringVar())
        checkbox_var_list[len(checkbox_var_list)-1].set('0')
        checkbox_list.append(tk.Checkbutton(self.AddParticipant_window, variable=checkbox_var_list[len(checkbox_var_list)-1], onvalue=1, offvalue=0, text='Zu Kurs hinzufügen?'))

        self.checkbox_list = checkbox_list
        self.checkbox_var_list = checkbox_var_list

        self.SubmitButton = tk.Button(self.AddParticipant_window, text='Änderungen speichern', command=self.submit_changes)
        self.SubmitButton.grid(column=start_column, row=len(self.students_info)+3)

    def delete_widgets_in_grid(self):
        for widget in self.new_stud_widget_list:
            widget.destroy()

    def show_new_student_widgets(self):
        start_column = 0
        if self.add_new_student_to_system.get() == '1':
            i = 1
            for obj in self.new_stud_widget_list:
                obj.grid(column=start_column+i, row=len(self.students_info)+2)
                i = i + 1
            self.checkbox_list[len(self.checkbox_list)-1].grid(column=start_column+5, row=len(self.students_info)+2)
        else:
            for obj in self.new_stud_widget_list:
                obj.grid_forget()
            self.checkbox_list[len(self.checkbox_list)-1].grid_forget()

    def submit_changes(self):
        for i, checkbox_var in enumerate(self.checkbox_var_list):
            if checkbox_var.get() == '1':
                sql_check_if_entry = "SELECT student_id FROM stud_courses WHERE student_id = ? AND course_id = ?"
                try:
                    stud_info = self.students_info[i][0]
                except:
                    stud_info = ''
                params_select_check = (stud_info, self.SelectedCourse_obj.Get_CourseID())
                returned_values = self.db_connection.GetFromDatabase(sql_check_if_entry, params_select_check)

                if len(returned_values) == 0:

                    sql_insert_into_stud_courses = "INSERT INTO stud_courses (student_id, course_id) VALUES (?, ?)"
                    self.db_connection.addToDatabase(sql_insert_into_stud_courses, params_select_check)
        self.delete_widgets_in_grid()
        self.build_grid()

        # if checkbox for new participant is activated write new student to table
        if self.add_new_student_to_system.get() == '1':
            new_stud = Student(self.new_stud_var_list[0].get(), self.new_stud_var_list[1].get(), self.new_stud_var_list[2].get(), self.new_stud_var_list[3].get())

        self.check_students_in_course()
        list = self.AddParticipant_window.grid_slaves()
        for element in list:
            element.destroy()
        self.build_grid()


    def get_current_value_dropdownMenu(self, value):
        self.selected_value_dropdownMenu = value


    def Show_Widgets(self):
        self.FornamePartEntry.pack()
        self.SurnamePartEntry.pack()
        self.YearPartEntry.pack()
        self.TutorPartEntry.pack()
        #self.SubmitNewParticipant.pack()

    def Hide_Widgets(self):
        self.FornamePartEntry.pack_forget()
        self.SurnamePartEntry.pack_forget()
        self.YearPartEntry.pack_forget()
        self.TutorPartEntry.pack_forget()
        #self.SubmitNewParticipant.pack_forget()

    def Check_Widgets(self):
        return self.FornamePartEntry.winfo_ismapped()

    def InspectNewParticipant_Entries(self):
        self.SubmitNewParticipant.pack_forget()
        if self.participant_shown.get() == 'Teilnehmenden hinzufügen':
            msg = f"""Soll der Kurs so eingetragen werden?
            \n Name: {self.FornamePartEntry.get()} {self.SurnamePartEntry.get()}
            \n Klassenstufe: {self.YearPartEntry.get()}
            \n Tutor: {self.TutorPartEntry.get()}"""
            user_return = tkinter.messagebox.askyesno(title='Teilnehmer erstellen & eintragen?', message=msg)
            if user_return is True:
                #pdb.set_trace()
                self.AddedStudent = Student(self.NewPartForname.get(), self.NewPartSurname.get(), self.NewPartYear.get(), self.NewPartTutor.get())
                self.SelectedCourse_obj.AddStudent(self.AddedStudent.Get_ID())
                self.AddParticipant_window.destroy()
                self.Update()

        else:
            self.Hide_Widgets()
            first_dot_pos = self.selected_value_dropdownMenu.find(',')
            Selected_studentID = self.selected_value_dropdownMenu[0:first_dot_pos]
            print(Selected_studentID)
            self.SelectedCourse_obj.AddStudent(Selected_studentID)
            self.AddParticipant_window.destroy()

    def InspectParticipantsDropDown(self, event):
        if self.participant_shown.get() == 'Teilnehmenden hinzufügen':
            if self.Check_Widgets() == 0:
                self.Show_Widgets()
        else:
            self.Hide_Widgets()
            self.AddedStudent = Student(self.participants_list[0][1], self.participants_list[0][2], self.participants_list[0][3], self.participants_list[0][4])
            self.SelectedCourse_obj.AddStudent(self.AddedStudent.Get_ID())
            # If a already existent participant is selected, he gets add to the Course
            # Decompose String to Tupel
            # dec_string = self.participant_shown
            # selection = dec_string[0:dec_string.find(',')]


def ManageCourses(db_connection):

    root1 = tk.Toplevel()

    # Initalise the Frames which split the Window
    DropdownMenuFrame = tk.Frame(root1)
    CourseInfoFrame = tk.Frame(root1)
    PieFrame = tk.Frame(root1)
    AddParticipantFrame = tk.Frame(root1)

    # Draw the Frames:
    DropdownMenuFrame.grid(column=0, row=0)
    CourseInfoFrame.grid(column=0, row=1)
    PieFrame.grid(column=1, row=1)
    AddParticipantFrame.grid(column=0, row=2)

    # the frame objects are stored in a list and given to the other classes

    FrameList = [DropdownMenuFrame, CourseInfoFrame, PieFrame, AddParticipantFrame]

    DropDownMenu = CoursesDropdown_menu(db_connection, FrameList)
    root1.mainloop()

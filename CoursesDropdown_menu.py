import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox

from Course import Course
from CourseInfo import CourseInfo


class CoursesDropdown_menu:

    def __init__(self, db_connection, Framelist, child_window, current_display_size):


        DropdownMenuFrame = Framelist[0]
        CourseInfoFrame = Framelist[1]
        PieFrame = Framelist[2]
        AddParticipantFrame = Framelist[3]
        calender_frame = Framelist[4]
        self.FrameList = [DropdownMenuFrame, CourseInfoFrame, PieFrame, AddParticipantFrame, calender_frame]
        self.courseInfo = None
        self.CourseObj = None
        self.widget_dropdown_CourseNames = None
        self.db_connection = db_connection
        self.DropdownMenuFrame = DropdownMenuFrame
        self.child_window = child_window
        self.current_display_size = current_display_size
        self.calender_frame = calender_frame

        # init heading frame and scrollbars:
        self.drop_down_heading_frame = tk.Frame(self.DropdownMenuFrame, width=current_display_size[0]/2, height=50)
        self.dropdown_heading_label = ttk.Label(self.DropdownMenuFrame, text='Ausgewählter Kurs', style="My.TLabel")
        self.dropdown_heading_label.grid(column=0, row=0, sticky='n')

        self.drop_down_frame_canvas = tk.Canvas(self.DropdownMenuFrame, width=current_display_size[0]/2)
        self.drop_down_frame_canvas.grid(column=0, row=1, sticky='nw')
        # create a horizontal scrollbar for the course info Frame:
        self.dropdown_hscrollbar = tk.Scrollbar(self.DropdownMenuFrame, orient=tk.HORIZONTAL, command=self.drop_down_frame_canvas.xview)
        self.dropdown_hscrollbar.grid(column=0, row=2, columnspan=2, sticky='ew')

        self.dropdown_vscrollbar = tk.Scrollbar(self.DropdownMenuFrame, orient=tk.VERTICAL, command=self.drop_down_frame_canvas.yview)
        self.dropdown_vscrollbar.grid(column=2, row=0, sticky='e', rowspan=2)

        # configure the axes
        self.drop_down_frame_canvas.configure(xscrollcommand=self.dropdown_hscrollbar.set, scrollregion=(0, 0, 2000,2000), yscrollcommand=self.dropdown_vscrollbar.set)
        self.drop_down_frame_canvas.bind('<Configure>', lambda e: self.drop_down_frame_canvas.bbox("all"))
        # course_info_frame_canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.dropdown_second_frame = tk.Frame(self.drop_down_frame_canvas, bd=1, relief=tk.SUNKEN)

        self.drop_down_frame_canvas.create_window((0, 0), window=self.dropdown_second_frame, anchor='nw')

        DropdownMenuFrame = self.dropdown_second_frame

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

        # call CourseInfo at init, so CourseInfo Frame holds data when the window pops up:
        self.InspectDropdownValue()


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
        user_return = tkinter.messagebox.askyesno(title='Kurs löschen?', message=msg, parent=self.child_window)
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
        user_return = tkinter.messagebox.askyesno(title='Kurs eintragen?', message=msg, parent=self.child_window)
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

            # # get the current screen size:
            # current_display_size = get_display_size()

            #self.child_window.geometry(f"{current_display_size[0]}x{current_display_size[1]}")
            self.courseInfo = CourseInfo(self.db_connection, self.CourseObj, self.FrameList, self.child_window, self.current_display_size)
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
        user_return = tkinter.messagebox.askyesno(title='Kurs eintragen?', message=msg, parent=self.child_window)
        if user_return is True:
            # set CourseId -1 if its a new Course
            self.SelectedCourse = Course(self.db_connection, CourseName, Year, Contact, Notes, -1)

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
        CourseInfo(self.db_connection, self.SelectedCourse, self.FrameList, self.child_window, self.current_display_size)

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

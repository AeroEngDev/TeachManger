import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
from tkinter import filedialog
import datetime as dt
import os as os

from PieChart import PieChart
from Student import Student
from interact_with_excel import excel_interact
from read_mode import read_mode

import pdb


class CourseInfo:

    def __init__(self, db_connection, SelectedCourse_obj, root, child_window, current_display_size):
        self.db_connection = db_connection
        self.Frame_Obj = root
        self.root = root[1]
        self.PieFrame = root[2]
        self.MaintanceFrame = root[3]
        self.CourseName = SelectedCourse_obj.Get_CourseName()
        self.SelectedCourse_obj = SelectedCourse_obj
        self.child_window = child_window

        # init heading frame and scrollbars:
        self.CourseInfoFrame = self.root
        self.course_info_heading_frame = tk.Frame(self.CourseInfoFrame, width=current_display_size[0]/2, height=50, relief=tk.SUNKEN, bd=1)
        self.course_info_heading_frame.grid(column=0, row=0, sticky='n')

        photo = tk.PhotoImage(file="plus_button.gif")
        self.plus_button = tk.Button(self.course_info_heading_frame, image=photo, command=self.Start_AddPart)
        self.plus_button.image = photo
        self.plus_button.grid(column=1, row=0)

        view_mode_photo = tk.PhotoImage(file="switch_to_view_mode.gif")
        self.view_mode_button = tk.Button(self.course_info_heading_frame, image=view_mode_photo, command=self.click_view_mode_button)
        self.view_mode_button.image = view_mode_photo
        self.view_mode_button.grid(column=2, row=0)

        edit_mode_photo = tk.PhotoImage(file="edit_pictogram.gif")
        self.edit_mode_button = tk.Button(self.course_info_heading_frame, image=edit_mode_photo, command=self.click_edit_mode_button)
        self.edit_mode_button.image = edit_mode_photo
        #self.view_mode_button.grid(column=2, row=0)

        # Button for exporting the sheet to excel
        export_excel_photo = tk.PhotoImage(file="excel_export.gif")
        self.excel_export_button = tk.Button(self.course_info_heading_frame, text="Excel", command=self.open_excel_window, image=export_excel_photo)
        self.excel_export_button.image = export_excel_photo
        self.excel_export_button.grid(column=3, row=0)

        self.label_heading_student_info = ttk.Label(self.course_info_heading_frame, text='Teilnehmende und Notenpunkte im Kurs', style="My.TLabel")
        self.label_heading_student_info.grid(column=4, row=0)
        # to make the scrollbar happen, we need a canvas inside the course info frame
        self.course_info_frame_canvas = tk.Canvas(self.CourseInfoFrame, width=current_display_size[0]/2, height=500)
        self.course_info_frame_canvas.grid(column=0, row=1, sticky='nw')
        # create a horizontal scrollbar for the course info Frame:
        self.hscrollbar = tk.Scrollbar(self.CourseInfoFrame, orient=tk.HORIZONTAL, command=self.course_info_frame_canvas.xview)
        self.hscrollbar.grid(column=0, row=2, columnspan=2, sticky='ew')

        self.vscrollbar = tk.Scrollbar(self.CourseInfoFrame, orient=tk.VERTICAL, command=self.course_info_frame_canvas.yview)
        self.vscrollbar.grid(column=2, row=0, sticky='e', rowspan=2)

        # configure the axes
        self.course_info_frame_canvas.configure(xscrollcommand=self.hscrollbar.set, scrollregion=(0, 0, 2000,2000), yscrollcommand=self.vscrollbar.set)
        self.course_info_frame_canvas.bind('<Configure>', lambda e: self.course_info_frame_canvas.bbox("all"))
        # course_info_frame_canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.second_frame = tk.Frame(self.course_info_frame_canvas, bd=1, relief=tk.SUNKEN)

        self.course_info_frame_canvas.create_window((0, 0), window=self.second_frame, anchor='nw')

        # Initalise The Pie Chart:
        self.PieChart_obj = PieChart(self.PieFrame, self.db_connection, self.SelectedCourse_obj, self)
        self.PieChart_obj.init_event_handlers()
        self.dict_child_grade_id_matplotlib_obj = self.PieChart_obj.dict_child_grade_id_matplotlib_obj

        self.root = self.second_frame

        # Get the Infos about this course ouf of the db
        self.GET_CourseInfo()

        # init the view mode:
        self.read_mode_obj = read_mode(self.root)
        self.view_treeview_obj = self.read_mode_obj.build_treeview(self.dict_view_mode)
        #MaintainCourses_Menu(self.Frame_Obj, db_connection, self.SelectedCourse_obj, self.edited_text, self.entryWidget_list, self, child_window)

    def open_excel_window(self):
        self.active_widgets_import_export = []
        self.excel_window = tk.Toplevel(self.child_window)
        self.excel_window_heading_frame = tk.Frame(self.excel_window)
        self.excel_window_heading_frame.grid(column=0, row=0)

        self.label_heading = ttk.Label(self.excel_window_heading_frame, text='Excel Import & Export', style="My.TLabel")
        self.label_heading.grid(column=0, row=0)

        self.excel_window_content_frame = tk.Frame(self.excel_window)
        self.excel_window_content_frame.grid(column=0, row=1)

        self.label_desc_ask_what_to_do = tk.Label(self.excel_window_content_frame, text='Was möchtest du tun?')
        self.label_desc_ask_what_to_do.grid(column=0, row=0)

        self.sel_import_export = tk.IntVar()
        self.radio_import  = tk.Radiobutton(self.excel_window_content_frame, text='Import', variable=self.sel_import_export, value=1, command=self.activate_widgets)
        self.radio_import.grid(column=1, row=0)

        self.radio_export = tk.Radiobutton(self.excel_window_content_frame, text='Export', variable=self.sel_import_export, value=2, command=self.activate_widgets)
        self.radio_export.grid(column=2, row=0)

        # define import widgets:
        self.button_start_openfile_dialog = tk.Button(self.excel_window_content_frame, text='Öffnen', command=self.excel_window_open_dialog)

        self.entry_excel_filename_var = tk.StringVar()
        self.entry_excel_filename = tk.Entry(self.excel_window_content_frame, textvariable=self.entry_excel_filename_var, width=50)

        self.submit_open_command = tk.Button(self.excel_window_content_frame, text='Datei importieren', command=self.import_excel_file)

        self.descr_label = tk.Label(self.excel_window_content_frame, text='Bitte gib einen Dateinamen an:')


        self.file_name_var = tk.StringVar()
        self.file_name_var.set(self.build_distinct_file_name())
        self.file_name_entry = tk.Entry(self.excel_window_content_frame, textvariable=self.file_name_var)


        self.label_desc_radio_buttons = tk.Label(self.excel_window_content_frame, text='Wähle aus, was exportiert werden soll')


        self.check_buttons_list = []
        self.check_box_var_list = []

        for column in self.dict_view_mode.keys():
            self.check_box_var_list.append(tk.IntVar())
            self.check_buttons_list.append(tk.Checkbutton(self.excel_window_content_frame, text=column, variable=self.check_box_var_list[len(self.check_box_var_list)-1]))

        self.check_box_var_list.append(tk.IntVar())
        self.check_buttons_list.append(tk.Checkbutton(self.excel_window_content_frame, text='Exportiere Notengewichtungsschaubild', variable=self.check_box_var_list[len(self.check_box_var_list)-1]))


        self.submit_button = tk.Button(self.excel_window_content_frame, text='Abschicken', command=self.submit_excel_export)


    def excel_window_open_dialog(self):
        self.excel_filename = filedialog.askopenfilename(initialdir=os.getcwd(), title='Exceldokument importieren', filetypes=(("xls Erweiterung", "*.xls"), ("xlsx Erweiterung", "*.xlsx")))
        self.entry_excel_filename_var.set(self.excel_filename)

    def activate_widgets(self):
        # hide the widgets that were active from last selection:
        for widget in self.active_widgets_import_export:
            widget.grid_forget()

        self.active_widgets_import_export = []

        if self.sel_import_export.get() == 1:
            # put the import widgets on screen
            self.button_start_openfile_dialog.grid(column=0, row=1)
            self.entry_excel_filename.grid(column=1, row=1)
            self.submit_open_command.grid(column=0, row=2)

            self.active_widgets_import_export = [self.button_start_openfile_dialog, self.entry_excel_filename, self.submit_open_command]
        elif self.sel_import_export.get() == 2:
            self.descr_label.grid(column=0, row=1)
            self.active_widgets_import_export.append(self.descr_label)
            self.file_name_entry.grid(column=1, row=1)
            self.active_widgets_import_export.append(self.file_name_entry)
            self.label_desc_radio_buttons.grid(column=1, row=2)
            self.active_widgets_import_export.append(self.label_desc_radio_buttons)
            for i, check_button in enumerate(self.check_buttons_list):
                check_button.grid(column=1, row=3+i)
                self.active_widgets_import_export.append(check_button)
            self.submit_button.grid(column=1, row=4+i)
            self.active_widgets_import_export.append(self.submit_button)

    def import_excel_file(self):
        widgets_in_content_frame = self.excel_window_content_frame.winfo_children()
        for widget in widgets_in_content_frame:
            widget.grid_forget()
        self.desc_for_imported_data = tk.Label(self.excel_window_content_frame, text=f'Eingelesene Daten aus {self.excel_filename}:')
        self.desc_for_imported_data.grid(column=0, row=0)
        excel_obj = excel_interact(self.excel_filename)
        self.spreadsheet_data_dict = excel_obj.read()

        treeview_of_spreadsheet = read_mode(self.excel_window_content_frame)
        self.treeview_spreadsheet_data_widget = treeview_of_spreadsheet.build_treeview(self.spreadsheet_data_dict)
        self.treeview_spreadsheet_data_widget.grid(column=0, row=1)

        # iterate through the columns, get the postition of the columns and place a Checkbutton:
        self.checkbutton_of_imported_columns = []
        for column_name in self.spreadsheet_data_dict.keys():
            self.position = self.treeview_spreadsheet_data_widget.bbox(item='0', column=column_name)
            self.checkbutton_of_imported_columns.append(tk.Checkbutton(self.excel_window_content_frame, text=''))
            try:
                self.checkbutton_of_imported_columns[len(self.checkbutton_of_imported_columns)-1].place(x=self.position[0], y=self.position[1])
            except:
                pass
        self.compare_import_data_and_db_data()

    def compare_import_data_and_db_data(self):
        self.status_label_check_headings_of_imported_data = tk.Label(self.excel_window_content_frame, text='Vergleiche die Spalten Namen des Spreadsheets mit denen der Datenbank...')
        self.status_label_check_headings_of_imported_data.grid(column=0, row=2)

        imported_column_label_list = []
        list_of_listboxes = []
        list_of_listboxes_var = []
        option_menu_items = list(self.dict_view_mode.keys())
        for imported_column in self.spreadsheet_data_dict.keys():
            imported_column_label_list.append(tk.Label(self.excel_window_content_frame, text=imported_column))
            imported_column_label_list[len(imported_column_label_list)-1].grid(column=0, row=3+len(imported_column_label_list)-1)
            arrow = tk.Label(self.excel_window_content_frame, text='->')
            arrow.grid(column=1, row=3+len(imported_column_label_list)-1)
            list_of_listboxes_var.append(tk.StringVar())
            list_of_listboxes.append(tk.OptionMenu(self.excel_window_content_frame, list_of_listboxes_var[len(list_of_listboxes_var)-1], *option_menu_items))

            list_of_listboxes[len(list_of_listboxes)-1].grid(column=2, row=3+len(imported_column_label_list)-1)
            if imported_column in self.dict_view_mode.keys():
                list_of_listboxes_var[len(list_of_listboxes_var)-1].set(imported_column)


    def submit_excel_export(self):
        self.excel_window_obj = excel_interact(self.file_name_var.get())

        dict_values_for_excel = {}
        # check which checkbox is ticked and write the column in dict:
        for button_number, check_button_var in enumerate(self.check_box_var_list):
            value = check_button_var.get()
            if value == 1:
                dict_values_for_excel[self.check_buttons_list[button_number].cget('text')] = self.dict_view_mode[self.check_buttons_list[button_number].cget('text')]

        self.excel_window_obj.create(dict_values_for_excel)
        os.system(f'libreoffice {self.file_name_var.get()}')

    def build_distinct_file_name(self):
        current_time = dt.datetime.now()
        current_time_str = current_time.strftime("%d%m%Y_%H%M%S")
        return f"{self.CourseName}_{current_time_str}.xlsx"

    def click_edit_mode_button(self):
        self.view_treeview_obj.grid_forget()
        self.edit_mode_button.grid_forget()
        self.view_mode_button.grid(column=2, row=0)
        self.GET_CourseInfo()

    def click_view_mode_button(self):

        #self.Clear_Frame()
        #self.read_mode_obj.show()
        for widget_list in self.entryWidget_list:
            for widget in widget_list:
                widget.grid_forget()
        for widget in self.column_desc_list:
            widget.grid_forget()
        self.view_treeview_obj.grid(column=0, row=0)
        self.view_mode_button.grid_forget()
        self.edit_mode_button.grid(column=2, row=0)

    def Start_AddPart(self):
        AddParticipant(self.db_connection, self.SelectedCourse_obj, self, self.child_window)

    def GET_CourseInfo(self):

        # Inner Join, get student_id and Student Names
        sql_get_course_content = "SELECT stud_courses.student_id, Students.forname, Students.surname FROM stud_courses INNER JOIN Students ON Students.student_id = stud_courses.student_id WHERE stud_courses.course_id = ?"
        student_ids_in_course = self.db_connection.GetFromDatabase(sql_get_course_content, (self.SelectedCourse_obj.Get_CourseID(),))
        student_ids_in_course = list(dict.fromkeys(student_ids_in_course))

        # get the grades out of the junktion table

        dict_student_grade_id_value = {}
        for student in student_ids_in_course:
            dict_student_grade_id_value[student[0]] = {}
            sql_get_grades_for_id = "SELECT grade_id, grade_value FROM stud_courses_grades WHERE student_id = ? AND course_id = ?"
            grades_for_student_id = self.db_connection.GetFromDatabase(sql_get_grades_for_id, (student[0], self.SelectedCourse_obj.Get_CourseID()))
            dict_grade_id_grade_value = {}
            for grade in grades_for_student_id:
                dict_grade_id_grade_value[grade[0]] = grade[1]
            dict_student_grade_id_value[student[0]] = dict_grade_id_grade_value

        # get the weights and the grade names
        grade_names = {}
        grade_weights = {}
        sql_get_weight_names = "SELECT grade_id, grade_name, grade_weight, child_of FROM Grades WHERE course_id = ?"
        grade_info_course = self.db_connection.GetFromDatabase(sql_get_weight_names, (self.SelectedCourse_obj.Get_CourseID(),))
        for row in grade_info_course:
            if row[0] != row[3]:
                grade_names[row[0]] = row[1]
                grade_weights[row[0]] = row[2]
        self.dict_student_grade_id_value = dict_student_grade_id_value
        self.student_ids_in_course = student_ids_in_course
        #self.grades_of_students_in_course = grades_of_students_in_course
        self.grade_names = grade_names
        self.grade_weights = grade_weights

        # build the dict for the view-mode:
        self.dict_view_mode = {}
        self.dict_view_grades = {}

        for grade_key, grade_name in self.grade_names.items():
            self.dict_view_grades[grade_key] = []

        id_list = []
        forname_list = []
        surname_list = []
        for student in self.student_ids_in_course:
            id_list.append(student[0])
            forname_list.append(student[1])
            surname_list.append(student[2])
            for grade_key in self.dict_view_grades.keys():
                if grade_key in self.dict_student_grade_id_value[student[0]]:
                    self.dict_view_grades[grade_key].append(self.dict_student_grade_id_value[student[0]][grade_key])
                else:
                    self.dict_view_grades[grade_key].append('')

        self.dict_view_mode['ID'] = id_list
        self.dict_view_mode['Vorname'] = forname_list
        self.dict_view_mode['Nachname'] = surname_list

        for key, value in self.dict_view_grades.items():
            self.dict_view_mode[self.grade_names[key]] = value


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

        if len(self.student_ids_in_course) != 0:
            try:
                columns = len(self.grades_of_students_in_course[0])
            except:
                columns = 0

            # sql_get_grade_info = "SELECT grade_id, grade_name, grade_weight FROM Grades WHERE course_id = ?"
            # get_grade_info = self.db_connection.GetFromDatabase(sql_get_grade_info, (self.SelectedCourse_obj.Get_CourseID(),))

            self.entryWidget_list = []
            self.edited_text = []
            self.column_desc_list = []
            self.column_desc_list.append(tk.Label(self.root, text='Student ID'))
            self.column_desc_list[0].grid(row=0, column=0)
            self.column_desc_list.append(tk.Label(self.root, text='Vorname'))

            self.column_desc_list[1].grid(row=0, column=1)
            self.column_desc_list.append(tk.Label(self.root, text='Nachname'))
            self.column_desc_list[2].grid(row=0, column=2)

            i = 1
            for grade_id, grade_name in self.grade_names.items():
                self.column_desc_list.append(tk.Label(self.root, text=f"{grade_id}, {grade_name}"))

                self.column_desc_list[2+i].grid(row=0, column=2+i)
                i = i+1

            self.column_desc_list.append(tk.Label(self.root, text='Gesamtpunkte'))
            self.column_desc_list[len(self.column_desc_list)-1].grid(row=0, column=len(self.column_desc_list)-1)

            self.column_desc_list.append(tk.Label(self.root, text='Löschen'))
            self.column_desc_list[len(self.column_desc_list)-1].grid(row=0, column=len(self.column_desc_list)-1)
            # a dict where the keys are the stud_id and the values are the end grade:
            self.dict_stud_id_end_grade = {}

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
                end_grade = 0
                for grade_id, grade_name in self.grade_names.items():
                    self.edited_text_set.append(tk.StringVar())
                    self.entryWidget_list_set.append(tk.Entry(self.root, textvariable=self.edited_text_set[len(self.edited_text_set)-1]))
                    self.entryWidget_list_set[len(self.entryWidget_list_set)-1].bind("<Return>", lambda event: self.Update(event))
                    self.entryWidget_list_set[len(self.entryWidget_list_set)-1].grid(column=2+j, row=i+1)
                    # insert grade for the grade_id
                    for key, value in self.dict_student_grade_id_value[student[0]].items():
                        if key == grade_id:
                            self.edited_text_set[len(self.edited_text_set)-1].set(value)
                            #pdb.set_trace()
                            end_grade = end_grade + float(self.dict_child_grade_id_matplotlib_obj[key].get_text()[0:len(self.dict_child_grade_id_matplotlib_obj[key].get_text())-1])/100*value

                    j = j + 1

                self.edited_text_set.append(tk.StringVar())
                self.entryWidget_list_set.append(tk.Label(self.root, text=round(end_grade, 2)))
                self.entryWidget_list_set[len(self.entryWidget_list_set)-1].grid(column=len(self.entryWidget_list_set)-1, row=i+1)

                # build a end_grade_dict, where the keys are the stud_id and the values are the end grade
                self.dict_stud_id_end_grade[student[0]] = end_grade

                # create a tk image obj
                remove_button_image = tk.PhotoImage(file=r"remove_button.gif")

                def func_button(event, self=self, i=i):
                    self.remove_stud_from_course(i)

                self.entryWidget_list_set.append(tk.Button(self.root, image=remove_button_image))
                self.entryWidget_list_set[len(self.entryWidget_list_set)-1].grid(column=len(self.entryWidget_list_set)-1, row=i+1)
                self.entryWidget_list_set[len(self.entryWidget_list_set)-1].bind('<Button-1>', func_button)
                # take a extra reference to the image, so the image wont be garbage collected
                self.entryWidget_list_set[len(self.entryWidget_list_set)-1].image = remove_button_image

                self.edited_text.append(self.edited_text_set)
                self.entryWidget_list.append(self.entryWidget_list_set)

            return self.edited_text, self.entryWidget_list
        else:
            self.no_students_in_course_label = tk.Label(self.root, text='Keine Teilnehmenden im Kurs. Bitte neue Teilnehmende hinzufügen!')
            self.no_students_in_course_label.pack()
            return [], []

    def calc_end_grade_current_row(self, current_row):
        pass


    def calc_end_grade(self):
        for current_row, student_id in enumerate(self.student_ids_in_course):
            if student_id in self.dict_student_grade_id_value.keys():
                value_dict = self.dict_student_grade_id_value[student_id]

                hallo = self.entryWidget_list[current_row]
                end_grade = 0
                for i, key_grade_id, value_grade_value in enumerate(value_dict.items()):
                    end_grade = end_grade + float(self.dict_child_grade_id_matplotlib_obj[5].get_text()[0:len(self.dict_child_grade_id_matplotlib_obj[5].get_text())-1])/100*value_grade_value
        row_pos = 1
        # for key_stud_id, value_dict in self.dict_student_grade_id_value.items():
        #
        #
        #     row_pos = row_pos + 1


    def remove_stud_from_course(self, row_index):
        sql_delelte_stud_from_course = "DELETE FROM stud_courses WHERE student_id = ?"
        student_id = self.edited_text[row_index][0].get()
        self.db_connection.addToDatabase(sql_delelte_stud_from_course, (student_id,))
        self.Clear_CourseInfo()
        self.GET_CourseInfo()

    def Update(self, event):
        msg = """Bist du sicher, dass du die Änderungen so in die Datenbank schreiben möchtest? Alle Daten werden so in die Datenbank geschrieben!"""
        user_return = tkinter.messagebox.askyesno(title='Änderungen speichern?', message=msg, parent=self.child_window)
        if user_return is True:
            number_of_rows = len(self.edited_text)
            number_of_columns = len(self.edited_text[0])
            # a dataset is a whole row of the table, while a entry is just one entry of the table
            data_students = []
            data_grades = []
            for dataset in self.edited_text:
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
                        sql_check_if_grade_id_in_stud_courses_grades = "SELECT grade_value FROM stud_courses_grades WHERE grade_id = ? AND student_id = ?"
                        grade_value_for_grade_id = self.db_connection.GetFromDatabase(sql_check_if_grade_id_in_stud_courses_grades, (grade_id, student_id))

                        course_id = self.SelectedCourse_obj.Get_CourseID()
                        # get grade_value
                        if dataset[i].get() != '':
                            grade_value = int(dataset[i].get())
                        else:
                            grade_value = ''
                        if type(grade_value) == int:

                            if len(grade_value_for_grade_id) != 0:
                                if grade_value_for_grade_id[0][0] != int(grade_value):

                                    sql_update_grade_value_for_grade_id = f"""UPDATE stud_courses_grades SET student_id={student_id}, course_id={course_id}, grade_id={grade_id}, grade_value={grade_value} WHERE student_id={student_id} AND course_id={course_id} AND grade_id={grade_id}"""
                                    params = (student_id, str(course_id), grade_id, grade_value, student_id, str(course_id), grade_id)
                                    self.db_connection.addToDatabase(sql_update_grade_value_for_grade_id, ())
                            else:
                                sql_insert_into_stud_courses_grades = "INSERT INTO stud_courses_grades (student_id, course_id, grade_id, grade_value) VALUES (?, ?, ?, ?)"
                                params = (student_id, course_id, grade_id, grade_value)
                                self.db_connection.addToDatabase(sql_insert_into_stud_courses_grades, params)
            self.GET_CourseInfo()

        def __del__(self):
            for row in self.entryWidget_list:
                for widget in row:
                    widget.destroy()


class MaintainCourses_Menu(CourseInfo):

    def __init__(self, root, db_connection, SelectedCourse_obj, text_obj_of_entries, widget_objects_of_entries, courseInfo_obj, child_window):
        self.Frame_Obj = root
        self.root = root[3]
        self.db_connection = db_connection
        self. SelectedCourse_obj = SelectedCourse_obj

        self.child_window = child_window
        self.course_info_obj = courseInfo_obj

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
        add_part = AddParticipant(self.db_connection, self.SelectedCourse_obj, self.course_info_obj, self.child_window)

    def Start_Update(self):
        self.root = self.Frame_Obj[1]

        self.column_desc_list, self.edited_text = self.course_info_obj.Get_Vars()
        self.Update()


class AddParticipant(CourseInfo):

    def __init__(self, db_connection, SelectedCourse_obj, course_info_obj, child_window):

        self.SelectedCourse_obj = SelectedCourse_obj
        self.course_info_obj = course_info_obj
        self.child_window =  child_window

        self.db_connection = db_connection
        self.AddParticipant_window = tk.Toplevel()

        # get all students
        #get all students who are in the selected course
        self.build_grid_add_student()

    def check_students_in_course(self):
        sql_GET_students_info = "SELECT * FROM Students"
        self.students_info = self.db_connection.GetFromDatabase(sql_GET_students_info, ())

        sql_students_in_selected_course = "SELECT student_id FROM stud_courses WHERE course_id = ?"
        self.students_in_selected_course = self.db_connection.GetFromDatabase(sql_students_in_selected_course, (self.SelectedCourse_obj.Get_CourseID(),))
        list = []
        for student_id in self.students_in_selected_course:
            list.append(student_id[0])
        self.students_in_selected_course = list

    def build_grid_add_student(self):

        self.check_students_in_course()
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

        # Widgets_entry_list = []
        # Widgets_label_id_list = []
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

            def func_button(event, self=self, student_id=current_row[0]):
                self.delete_students_from_system(student_id)

            remove_button_image = tk.PhotoImage(file=r"remove_button.gif")
            delete_student_button = tk.Button(self.AddParticipant_window, image=remove_button_image)
            delete_student_button.bind("<Button-1>", func_button)
            delete_student_button.image = remove_button_image
            delete_student_button.grid(column=7, row=start_row+current_row_number+1)

            checkbox_list.append(tk.Checkbutton(self.AddParticipant_window, variable=checkbox_var_list[len(checkbox_var_list)-1], onvalue=1, offvalue=0, text='Zu Kurs hinzufügen?'))

            if current_row[0] in self.students_in_selected_course:
                checkbox_list[len(checkbox_list)-1].config(state=tk.DISABLED)
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

    def delete_students_from_system(self, student_id):
        sql_delete_student = "DELETE FROM Students WHERE student_id = ?"
        self.db_connection.addToDatabase(sql_delete_student, (student_id,))
        self.delete_widgets_in_grid()
        self.build_grid_add_student()
        self.course_info_obj.Clear_Frame()
        self.course_info_obj.GET_CourseInfo()

    def delete_widgets_in_grid(self):
        for widget in self.AddParticipant_window.winfo_children():
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
        # if checkbox for new participant is activated write new student to table
        if self.add_new_student_to_system.get() == '1':
            new_stud = Student(self.new_stud_var_list[0].get(), self.new_stud_var_list[1].get(), self.new_stud_var_list[2].get(), self.new_stud_var_list[3].get())

        self.check_students_in_course()
        for i, checkbox_var in enumerate(self.checkbox_var_list):
            if checkbox_var.get() == '1':
                sql_check_if_entry = "SELECT student_id FROM stud_courses WHERE student_id = ? AND course_id = ?"

                params_select_check = (self.students_info[i][0], self.SelectedCourse_obj.Get_CourseID())
                returned_values = self.db_connection.GetFromDatabase(sql_check_if_entry, params_select_check)

                if len(returned_values) == 0:

                    sql_insert_into_stud_courses = "INSERT INTO stud_courses (student_id, course_id) VALUES (?, ?)"
                    self.db_connection.addToDatabase(sql_insert_into_stud_courses, params_select_check)

        self.course_info_obj.GET_CourseInfo()

        # self.check_students_in_course()
        # list = self.AddParticipant_window.grid_slaves()
        # for element in list:
        #     element.destroy()
        # self.build_grid_add_student()
        self.AddParticipant_window.destroy()

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

    def Check_Widgets(self):
        return self.FornamePartEntry.winfo_ismapped()

    def InspectNewParticipant_Entries(self):
        self.SubmitNewParticipant.pack_forget()
        if self.participant_shown.get() == 'Teilnehmenden hinzufügen':
            msg = f"""Soll der Kurs so eingetragen werden?
            \n Name: {self.FornamePartEntry.get()} {self.SurnamePartEntry.get()}
            \n Klassenstufe: {self.YearPartEntry.get()}
            \n Tutor: {self.TutorPartEntry.get()}"""
            self.message_window = tk.window()
            self.message_window.attributes('-topmost', True)
            user_return = tkinter.messagebox.askyesno(title='Teilnehmer erstellen & eintragen?', message=msg, parent=self.child_window)
            if user_return is True:
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

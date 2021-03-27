import matplotlib.pyplot as plt  # plt is a Standard like np for numpy
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import *
import pdb
import numpy as np


class PieChart:

    def __init__(self, root, db_connection, Course_obj, courseinfo_obj):
        self.entry_field_new_wedge = None
        self.db_connection = db_connection
        self.Course_obj = Course_obj
        self.GET_grade_data()

        self.fig = Figure(figsize=(10, 5), dpi=100)
        self.axes = self.fig.add_axes([0.1, 0.1, 0.8, 0.8])

        # create a nested pie chart
        self.plot_pie()

        self.root = root

        canvas = FigureCanvasTkAgg(self.fig, master=root)
        canvas.get_tk_widget().pack()

        # save variables in self:
        #self.wedges = wedges

        self.canvas = canvas

        self.courseinfo_obj = courseinfo_obj
        self.AddParentGrade_Button = Button(self.root, text='Neue Notenkategorie hinzufügen', command=self.Add_Parent_Grade)
        self.AddGradeWeight_Button = Button(self.root, text='Neue Note hinzufügen', command=self.AddGrade_Weight)
        self.AddParentGrade_Button.pack()
        self.AddGradeWeight_Button.pack()
        #pdb.set_trace()

    def get_parent_grades(self):
            sql_select_parent_grade_info = "SELECT grade_id, grade_name, grade_weight FROM Grades WHERE grade_id = child_of"
            parent_grade_info = self.db_connection.GetFromDatabase(sql_select_parent_grade_info, ())
            return parent_grade_info

    def GET_grade_data(self):
        dict_parents_and_childs = {}
        dict_parent_weights = {}

        parent_grade_info = self.get_parent_grades()

        for parent_grade in parent_grade_info:
            dict_parents_and_childs[parent_grade[0]] = []
            dict_parent_weights[parent_grade[0]] = (parent_grade[0], parent_grade[1], parent_grade[2])

        sql_get_grade_weights_from_grades = """SELECT grade_id, grade_name, grade_weight, child_of FROM Grades WHERE course_id = ? """
        grade_names_and_weights = self.db_connection.GetFromDatabase(sql_get_grade_weights_from_grades, (self.Course_obj.Get_CourseID(),))
        grade_names = []
        grade_weights = []
        parent_weight_data = []

        for current in grade_names_and_weights:

            if current[3] == current[0]:
                pass
            else:
                dict_parents_and_childs[current[3]].append((current[0], current[1], current[2]))
                grade_weights.append(current[2])

        self.dict_parent_weights = dict_parent_weights
        self.dict_parents_and_childs = dict_parents_and_childs

        # save the parent grade data in a tuple
        parent_grade_weight_list = []
        parent_grade_name_list = []
        parent_names_only = []
        child_weight_list = []
        child_name_list = []
        for key, value in self.dict_parent_weights.items():
            parent_grade_weight_list.append(value[2])
            parent_grade_name_list.append(f"{value[0]}, {value[1]}")
            parent_names_only.append(value[1])

            list_grade_childs = self.dict_parents_and_childs[key]
            child_weight_list = []
            child_id_name_list = []
            child_name_list = []
            sum = 0
            for child_grade in list_grade_childs:
                sum = sum + child_grade[2]
                child_weight_list.append(child_grade[2])
                child_id_name_list.append(f"{child_grade[0]}, {child_grade[1]}")
                child_name_list.append(child_grade[1])

            if sum == 0:
                scale_factor = 0
            else:
                scale_factor = value[2]/sum

            for i, child in enumerate(child_weight_list):
                child = child*scale_factor
                child_weight_list[i] = child

        self.child_name_tuple = tuple(child_id_name_list)
        self.child_names_only = tuple(child_name_list)
        self.child_weight_tuple = tuple(child_weight_list)

        self.parent_grade_weight_tuple = tuple(parent_grade_weight_list)
        self.parent_grade_name_tuple = tuple(parent_grade_name_list)
        self.parent_names_only = tuple(parent_names_only)

        # self.parent_weight_data = parent_weight_data
        # self.WeightData = tuple(grade_weights)
        # self.WeightNames = tuple(grade_names)

    def plot_pie(self):

        pie_objs = []
        self.GET_grade_data()
        self.axes.clear()
        # create the outer pie:s
        self.outer_pie_objs = self.axes.pie(self.parent_grade_weight_tuple, radius=1, labels=self.parent_grade_name_tuple, wedgeprops=dict(edgecolor='w', width=0.3))
        self.outer_wedges = self.outer_pie_objs[0]
        pie_objs[0:0] = self.outer_wedges
        self.outer_wedges_names = self.outer_pie_objs[1]
        pie_objs[len(pie_objs):len(pie_objs)] = self.outer_wedges_names
        #pdb.set_trace()
        # create the inner pie
        self.inner_pie_objs = self.axes.pie(self.child_weight_tuple, radius=0.5, labels=self.child_name_tuple, autopct='%1.1f%%', wedgeprops=dict(edgecolor='w'))
        self.axes.set(aspect="equal", title='Notengewichtung')
        self.inner_wedges = self.inner_pie_objs[0]
        self.inner_wedges_names = self.inner_pie_objs[1]
        self.inner_procent_text = self.inner_pie_objs[2]

        pie_objs[len(pie_objs):len(pie_objs)] = self.inner_wedges
        pie_objs[len(pie_objs):len(pie_objs)] = self.inner_wedges_names
        for obj in pie_objs:
            obj.set_picker(True)

        self.fig.canvas.draw_idle()

    def Add_Parent_Grade(self):
        # # Build a distinct paretn grade name:
        # sql_count_objects_in_grades = "COUNT(SELECT grade_id FROM Grades)"
        # number_of_grades = self.db_connection.GetFromDatabase(sql_count_objects_in_grades, ())
        Default_Parent_Grade_Name = "Neue Notenkategorie"
        sql_add_parent_grade = "INSERT INTO Grades (grade_name, course_id, grade_weight) VALUES (?, ?, ?)"
        self.db_connection.addToDatabase(sql_add_parent_grade, (Default_Parent_Grade_Name, self.Course_obj.Get_CourseID(), 0.2))

        # get the grade_id of the inserted row:
        sql_get_grade_id = "SELECT last_insert_rowid()"
        grade_id_of_parent_grade = self.db_connection.GetFromDatabase(sql_get_grade_id, ())

        # set the grade a parent grade
        sql_update_parent_grade = "UPDATE Grades SET child_of = ? WHERE grade_id = ?"
        #pdb.set_trace()
        self.db_connection.addToDatabase(sql_update_parent_grade, (grade_id_of_parent_grade[0][0], grade_id_of_parent_grade[0][0]))

        self.plot_pie()

    def AddGrade_Weight(self):
        #for i, wedge in enumerate(self.wedges):

        label_desc_add_grade = Label(self.root, text='Zu welcher Notenkategorie soll die Note hinzugefügt werden?')
        label_desc_add_grade.pack()

        # get all parent grades:
        parent_grade_info = self.get_parent_grades()

        parent_grade_list = []
        for parent_grade in parent_grade_info:
            parent_grade_list.append(f"{parent_grade[0]}, {parent_grade[1]}")


        self.get_parent_grade_choice = StringVar()
        self.optionmenu_parent_grade = OptionMenu(self.root, self.get_parent_grade_choice, parent_grade_list[0], *parent_grade_list)
        self.optionmenu_parent_grade.pack()

        self.submit_new_grade = Button(self.root, text='Neue Note eintragen', command=self.submit)
        self.submit_new_grade.pack()

    def submit(self):
        sql_insert_grade_into_grades = """INSERT INTO Grades (grade_name, grade_weight, course_id, child_of) VALUES(?, ?, ?, ?)"""
        grade_id_grade_name = self.get_parent_grade_choice.get()
        pos_of_delimiter = grade_id_grade_name.find(',')
        grade_id = grade_id_grade_name[0:pos_of_delimiter]

        sql_params = ('Neue Note', 0.2, self.Course_obj.Get_CourseID(), grade_id)
        self.db_connection.addToDatabase(sql_insert_grade_into_grades, sql_params)

        #remove the buttons and optionMenu from screen
        self.optionmenu_parent_grade.pack_forget()
        self.submit_new_grade.pack_forget()

        # plot the new pie
        self.plot_pie()
        # update courseInfo Frame
        self.courseinfo_obj.Clear_CourseInfo()
        self.courseinfo_obj.GET_CourseInfo()

    def on_click(self, event):
        # screen position at which was clicked
        x_pos_of_clicking = event.mouseevent.x
        y_pos_of_clicking = event.mouseevent.y

        self.edited_weight = StringVar()
        self.edited_grade_name = StringVar()
        self.edited_parent_grade_name = StringVar()
        for wedge in self.inner_wedges:
            wedge.set_edgecolor('w')
            wedge.set_linewidth(1)

        for wedge in self.outer_wedges:
            wedge.set_edgecolor('w')
            wedge.set_linewidth(1)
        if self.entry_field_new_wedge is not None:
            self.entry_field_new_wedge.destroy()

        # has the description text been clicked?
        for i, text in enumerate(self.inner_wedges_names):
            if event.artist == text:
                self.edited_grade_name.set(self.child_names_only[i])
                self.edit_grade_name = Entry(self.canvas.get_tk_widget(), textvariable=self.edited_grade_name)
                self.edit_grade_name.place(x=x_pos_of_clicking, y=500-y_pos_of_clicking)
                self.Weight_pos = i

                def func(event):
                    self.update_grade_name(event, self.child_name_tuple, self.edited_grade_name, self.edit_grade_name)
                self.edit_grade_name.bind('<KeyPress>', func)

        for i, text in enumerate(self.outer_wedges_names):
            if event.artist == text:
                self.edited_parent_grade_name.set(self.parent_names_only[i])
                self.edit_grade_name = Entry(self.canvas.get_tk_widget(), textvariable=self.edited_parent_grade_name)
                self.edit_grade_name.place(x=x_pos_of_clicking, y=500-y_pos_of_clicking)
                self.Weight_pos = i

                def func(event):
                    self.update_grade_name(event, self.parent_grade_name_tuple, self.edited_parent_grade_name, self.edit_grade_name)
                self.edit_grade_name.bind('<KeyPress>', func)

        for i, wedge in enumerate(self.inner_wedges):

            if event.artist == wedge:
                wedge.set_edgecolor('red')
                wedge.set_linewidth(2)
                self.fig.canvas.draw_idle()
                for widget in self.root.winfo_children():
                    if isinstance(widget, Entry):
                        widget.pack_forget()

                self.edited_weight.set(str(self.child_weight_tuple[i]))
                self.entry_field_new_wedge = Entry(self.canvas.get_tk_widget(), textvariable=self.edited_weight)

                self.entry_field_new_wedge.place(x=x_pos_of_clicking, y=500-y_pos_of_clicking)
                self.Weight_pos = i

                def func(event):
                    self.entry_input_handler(event, 1)

                self.entry_field_new_wedge.bind('<KeyPress>', func)

        # check if the outer wedges were clicked
        for i, wedge in enumerate(self.outer_wedges):

            if event.artist == wedge:
                wedge.set_edgecolor('red')
                wedge.set_linewidth(2)
                self.fig.canvas.draw_idle()
                for widget in self.root.winfo_children():
                    if isinstance(widget, Entry):
                        widget.pack_forget()
                self.edited_weight.set(str(self.parent_grade_weight_tuple[i]))
                self.entry_field_new_wedge = Entry(self.canvas.get_tk_widget(), textvariable=self.edited_weight)
                self.entry_field_new_wedge.place(x=x_pos_of_clicking, y=500-y_pos_of_clicking)
                self.Weight_pos = i
                def func(event):
                    self.entry_input_handler(event, 2)

                self.entry_field_new_wedge.bind('<KeyPress>', func)

    def entry_input_handler(self, event, update_pos):
        # Weight_pos is the Position of the edit weight:
        i = self.Weight_pos
        if update_pos == 1:
            self.WeightData = self.child_weight_tuple
            weight_names = self.child_name_tuple
        else:
            self.WeightData = self.parent_grade_weight_tuple
            weight_names = self.parent_grade_name_tuple
        #pdb.set_trace()
        if event.keysym == 'Return':
            edited_weight = float(self.edited_weight.get())
            if isinstance(edited_weight, float):
                pos_of_delimiter = weight_names[i].find(',')
                grade_id = weight_names[i][0:pos_of_delimiter]
                sql_update_grade_weight = "UPDATE Grades SET grade_weight = ? WHERE grade_id = ?"
                params_for_update = (edited_weight, int(grade_id))
                #pdb.set_trace()
                self.db_connection.addToDatabase(sql_update_grade_weight, params_for_update)
                self.plot_pie()
            self.entry_field_new_wedge.destroy()


    def update_grade_name(self, event, list_of_grade_names, var_entry_field, entry_field):
        if event.keysym == 'Return':
            new_grade_name = var_entry_field.get()
            sql_update_grade_name = "UPDATE Grades SET grade_name = ? WHERE grade_id = ?"
            grade_id_pos = list_of_grade_names[self.Weight_pos].find(',')
            grade_id = list_of_grade_names[self.Weight_pos][0:grade_id_pos]
            pdb.set_trace()
            params = (new_grade_name, int(grade_id))
            #pdb.set_trace()
            self.db_connection.addToDatabase(sql_update_grade_name, params)
            entry_field.destroy()
            self.plot_pie()

    def init_event_handlers(self):
        self.fig.canvas.mpl_connect('pick_event', lambda event: self.on_click(event))
        # for wedge in self.wedges[0]:
        #     wedge.figure.canvas.mpl_connect('motion_notify_event', lambda event: self.moving_in(event))
            #wedge.fig.canvas.mpl_connect('motion_notify_event', lambda event)
        # self.fig.canvas.mpl_connect('motion_notify_event', lambda event: self.moving_in(event))
        # self.fig.canvas.mpl_connect('motion_notify_event', lambda event: self.moving_out(event))


# figure_graph = Figure(figsize = (5, 5), dpi = 100)
# #figure_graph = figure_graph.add_subplot()
# axes_graph = figure_graph.add_axes([0.1, 0.1, 0.8, 0.8])
# axes_graph.set_picker(True)
# slices = [0.12, 0.24, 0.14, 0.5]
# labels = ['Grade 1', 'Grade 2', 'Grade 3', 'Grade 4']
# wedges, text = axes_graph.pie(slices, labels=labels, shadow=True)
# for wedge in wedges:
#     wedge.set_picker(True)
# canvas = FigureCanvasTkAgg(figure_graph, master=root)
# canvas.get_tk_widget().pack()
# #toolbar.update()
# #canvas.get_tk_widget().pack()
# # plot1.title('Gewichtung der Noten:')
#     #plot1.show()
#
#
#
# def onclick(event, wedges, slices, labels):
#     #import pdb;
#     listofzeros = [0]*len(wedges)
#     for i, wedge in enumerate(wedges):
#
#         #pdb.set_trace()
#         if event.artist == wedge:
#             Label(root, text=f'clicked inside of {wedge}!').pack()
#             listofzeros[i] = 0.1
#             axes_graph.clear()
#             axes_graph.pie(slices, labels=labels, explode=listofzeros)
#             Entry(canvas, )
            # canvas = FigureCanvasTkAgg(figure_graph, master=root)
            # canvas.get_tk_widget().pack()

#GraphButton = Button(root, text='Plotte einen Graphen', command=onclick2).pack()
# root = Tk()
# pie_chart = PieChart('Geografie', [0.1, 0.1, 0.3, 0.2, 0.3], ['Mündlich Vortrag', 'Mündlich Mitarbeit', 'Mündlich Gruppenarbeit', 'Schriftlich HA Kontrolle', 'Schriftlich Klausur'])
# Button_Quit = Button(root, text='Quit', command=quit).pack()
#
# pie_chart.init_event_handlers()
#
# #cid = fig.canvas.mpl_connect('pick_event', lambda event: pie_chart.onclick(event))
# #pdb.set_trace()
#
# root.mainloop()

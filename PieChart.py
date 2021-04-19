import matplotlib.pyplot as plt  # plt is a Standard like np for numpy
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter as tk
import tkinter.ttk as ttk
import pdb
import numpy as np


class PieChart:

    def __init__(self, root, db_connection, Course_obj, courseinfo_obj):
        self.widgets_in_canvas = []
        self.widget_list_new_window = []
        self.widget_list_new_window_2 = []
        self.entry_field_new_wedge = None
        self.new_window = None
        self.db_connection = db_connection
        self.Course_obj = Course_obj
        self.new_window = tk.Toplevel()
        self.new_window.withdraw()

        self.outer_pie_objs = None

        self.GET_grade_data()

        self.fig = Figure(figsize=(10, 5), dpi=100)
        self.axes = self.fig.add_axes([0.1, 0.1, 0.8, 0.8])

        # create a nested pie chart
        self.plot_pie(1, 0, 0)

        self.root = root

        canvas = FigureCanvasTkAgg(self.fig, master=root)
        canvas.get_tk_widget().pack()

        # save variables in self:
        #self.wedges = wedges

        self.canvas = canvas

        self.courseinfo_obj = courseinfo_obj
        global photo
        photo = tk.PhotoImage(file="plus_button.gif")
        self.plus_button = tk.Button(self.canvas.get_tk_widget(), image=photo, command=self.new_window_for_new_grade)
        #self.plus_button.grid(column=0, row=0, stick='nw')
        self.plus_button.place(x=0, y=0)
        # create a slider to zoom in and out into the grade pie:
        self.zoom_slider = ttk.Scale(self.canvas.get_tk_widget(), from_=0.1, to=10, orient=tk.VERTICAL, command=self.zoom_with_mousewheel, length=300)
        #self.zoom_slider.grid(column=0, row=1, sticky="w")
        self.zoom_slider.place(x=0, y=100)

        # self.AddParentGrade_Button = tk.Button(self.canvas.get_tk_widget(), text='Neue Notenkategorie hinzufügen', command=self.Add_Parent_Grade)
        # self.AddGradeWeight_Button = tk.Button(self.canvas.get_tk_widget(), text='Neue Note hinzufügen', command=self.AddGrade_Weight)
        # self.AddParentGrade_Button.place(x=0, y=450)
        # self.AddGradeWeight_Button.place(x=300, y=450)

    def zoom_with_mousewheel(self, value):
        self.plot_pie(value, 0, 0)

    def new_window_for_new_grade(self):
        if tk.Toplevel.winfo_exists(self.new_window) == 0:
            self.new_window = tk.Toplevel()
        if self.new_window.state() == 'withdrawn':
            self.new_window.deiconify()
            self.new_window.attributes('-topmost', True)

        self.remove_widget_from_screen(self.widget_list_new_window_2)

        self.label_desc_new_grade = tk.Label(self.new_window, text="Hier können neue Noten und Notenkategorien festgelegt werden")
        self.label_desc_new_grade.pack()
        self.widget_list_new_window_2.append(self.label_desc_new_grade)

        self.label_desc_new_grade_2 = tk.Label(self.new_window, text="Was möchstest Du eintragen?")
        self.label_desc_new_grade_2.pack()
        self.widget_list_new_window_2.append(self.label_desc_new_grade)

        # check if there is already a Grade Parent. If no grade parent is present only
        # Grade Parents can be created
        grade_parents = self.get_parent_grades()
        if len(grade_parents) == 0:
            optionmenu_list = ['Neue Notenkategorie']
        else:
            optionmenu_list = ['Neue Notenkategorie', 'Neue Note']
        self.option_menu_val = tk.StringVar()
        self.new_window_option_menu = tk.OptionMenu(self.new_window, self.option_menu_val, *optionmenu_list)
        self.new_window_option_menu.pack()
        self.widget_list_new_window_2.append(self.new_window_option_menu)
        self.option_menu_val.trace("w", self.new_window_choice_made)

    def new_window_choice_made(self, *args):
        self.remove_widget_from_screen(self.widget_list_new_window)
        choice = self.option_menu_val.get()
        if choice == 'Neue Notenkategorie':
            self.Submit_new_parent_grade = tk.Button(self.new_window, text='Neue Notenkategorie eintragen', command=self.Add_Parent_Grade)
            self.Submit_new_parent_grade.pack()
            self.widget_list_new_window.append(self.Submit_new_parent_grade)
        else:
            self.AddGrade_Weight()

    def remove_widget_from_screen(self, widget_list):
        for widget in widget_list:
            widget.destroy()


    def get_parent_grades(self):
        sql_select_parent_grade_info = "SELECT grade_id, grade_name, grade_weight FROM Grades WHERE grade_id = child_of"
        parent_grade_info = self.db_connection.GetFromDatabase(sql_select_parent_grade_info, ())
        return parent_grade_info

    def GET_grade_data(self):
        dict_parents_and_childs = {}
        dict_parent_weights = {}

        dict_k_children_v_parent = {}

        parent_grade_info = self.get_parent_grades()

        for parent_grade in parent_grade_info:
            dict_parents_and_childs[parent_grade[0]] = []
            dict_parent_weights[parent_grade[0]] = (parent_grade[0], parent_grade[1], parent_grade[2])

        sql_get_grade_weights_from_grades = """SELECT grade_id, grade_name, grade_weight, child_of FROM Grades WHERE course_id = ? """
        grade_names_and_weights = self.db_connection.GetFromDatabase(sql_get_grade_weights_from_grades, (self.Course_obj.Get_CourseID(),))

        parent_id_list = []
        grade_weights = []
        self.dict_parent_id_child_wedges = {}
        for current in grade_names_and_weights:

            if current[3] == current[0]:
                pass
                parent_id_list.append(current[0])
                self.dict_parent_id_child_wedges[current[0]] = []
            else:
                dict_k_children_v_parent[current[0]] = current[3]
                dict_parents_and_childs[current[3]].append((current[0], current[1], current[2]))
                grade_weights.append(current[2])

        self.dict_parent_weights = dict_parent_weights
        self.dict_parents_and_childs = dict_parents_and_childs

        # save the parent grade data in a tuple
        parent_grade_weight_list = []
        parent_grade_name_list = []
        parent_names_only = []
        child_weight_list_all = []
        child_name_list = []
        child_id_name_list = []
        child_id_list = []
        for key, value in self.dict_parent_weights.items():
            parent_grade_weight_list.append(value[2])
            parent_grade_name_list.append(f"{value[0]}, {value[1]}")
            parent_names_only.append(value[1])
            child_weight_list = []
            list_grade_childs = self.dict_parents_and_childs[key]
            sum = 0

            for child_grade in list_grade_childs:
                sum = sum + child_grade[2]
                child_weight_list.append(child_grade[2])
                child_id_name_list.append(f"{child_grade[0]}, {child_grade[1]}")
                child_name_list.append(child_grade[1])
                child_id_list.append(child_grade[0])

            if not sum:
                scale_factor = 0
            else:
                scale_factor = value[2]/sum

            for i, child in enumerate(child_weight_list):
                child = child*scale_factor
                child_weight_list[i] = child
            child_weight_list_all.append(child_weight_list)

        child_list_weights = []

        for list in child_weight_list_all:
            for element in list:
                child_list_weights.append(element)

        self.child_id_list = tuple(child_id_list)
        self.child_name_tuple = tuple(child_id_name_list)
        self.child_names_only = tuple(child_name_list)
        self.child_weight_tuple = tuple(child_list_weights)

        self.parent_grade_weight_tuple = tuple(parent_grade_weight_list)
        self.parent_grade_name_tuple = tuple(parent_grade_name_list)
        self.parent_names_only = tuple(parent_names_only)

        self.dict_k_children_v_parent = dict_k_children_v_parent
        self.parent_id_list = parent_id_list


    def plot_pie(self, radius, dx, dy):

        # get the current center:
        if self.outer_pie_objs is not None:

            current_center = self.outer_pie_objs[0][0].center
        else:
            current_center = (0, 0)
        #pdb.set_trace()
        # calculate new center:
        new_center = ((current_center[0]+dx)*10, (current_center[1]+dy)*10)

        self.radius = float(radius)
        pie_objs = []
        self.GET_grade_data()
        self.axes.clear()

        colors = []
        for i in self.parent_grade_weight_tuple:
            colors.append('white')
        self.outer_pie_border = self.axes.pie(self.parent_grade_weight_tuple, colors=colors, center=new_center, radius=self.radius*1.3, wedgeprops=dict(edgecolor='b'))

        # create the outer pie:s
        self.outer_pie_objs = self.axes.pie(self.parent_grade_weight_tuple, radius=self.radius, center=new_center, labels=self.parent_grade_name_tuple, wedgeprops=dict(edgecolor='w', width=0.3))
        self.outer_wedges = self.outer_pie_objs[0]

        dict_parent_id_wedges = {}
        for i, parent_wedge in enumerate(self.outer_wedges):
            dict_parent_id_wedges[self.parent_id_list[i]] = parent_wedge

        pie_objs[0:0] = self.outer_wedges
        self.outer_wedges_names = self.outer_pie_objs[1]
        pie_objs[len(pie_objs):len(pie_objs)] = self.outer_wedges_names
        # create the inner pie
        self.inner_pie_objs = self.axes.pie(self.child_weight_tuple, radius=0.5*self.radius, center=new_center, labels=self.child_name_tuple, autopct='%1.1f%%', wedgeprops=dict(edgecolor='w'))
        self.axes.set(aspect="equal", title='Notengewichtung')
        self.inner_wedges = self.inner_pie_objs[0]


        # dict_parent_id_child_wedges = {}
        for i, matplotlib_wedge in enumerate(self.inner_wedges):
            grade_id = self.child_id_list[i]
            parent_id = self.dict_k_children_v_parent[grade_id]
            self.dict_parent_id_child_wedges[parent_id].append(matplotlib_wedge)

        for key, value in self.dict_parent_id_child_wedges.items():
            parent_wedge = dict_parent_id_wedges[key]
            try:
                start_angle = parent_wedge.theta1
                end_angle = parent_wedge.theta2
            except:
                start_angle = 0
            current_start_angle = start_angle
            for child_widget in value:
                child_widget.set_theta1(current_start_angle)
                current_start_angle = child_widget.theta2

        self.inner_wedges_names = self.inner_pie_objs[1]
        self.inner_procent_text = self.inner_pie_objs[2]

        self.dict_child_grade_id_matplotlib_obj = {}
        for i, matplotlib_pro_text in enumerate(self.inner_procent_text):
            grade_id = self.child_id_list[i]
            self.dict_child_grade_id_matplotlib_obj[grade_id] = matplotlib_pro_text


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
        sql_add_parent_grade = "INSERT INTO Grades (grade_name, course_id, grade_weight, child_of) VALUES (?, ?, ?, ?)"
        self.db_connection.addToDatabase(sql_add_parent_grade, (Default_Parent_Grade_Name, self.Course_obj.Get_CourseID(), 0.2, 0))

        # get the grade_id of the inserted row:
        sql_get_grade_id = "SELECT last_insert_rowid()"
        grade_id_of_parent_grade = self.db_connection.GetFromDatabase(sql_get_grade_id, ())

        # set the grade a parent grade
        sql_update_parent_grade = "UPDATE Grades SET child_of = ? WHERE grade_id = ?"

        self.db_connection.addToDatabase(sql_update_parent_grade, (grade_id_of_parent_grade[0][0], grade_id_of_parent_grade[0][0]))

        self.plot_pie(self.zoom_slider.get())
        self.new_window.destroy()

    def AddGrade_Weight(self):

        self.label_desc_add_grade = tk.Label(self.new_window, text='Zu welcher Notenkategorie soll die Note hinzugefügt werden?')
        self.label_desc_add_grade.pack()
        self.widget_list_new_window.append(self.label_desc_add_grade)

        # get all parent grades:
        parent_grade_info = self.get_parent_grades()

        parent_grade_list = []
        for parent_grade in parent_grade_info:
            parent_grade_list.append(f"{parent_grade[0]}, {parent_grade[1]}")
        self.get_parent_grade_choice = tk.StringVar()
        self.get_parent_grade_choice.set(parent_grade_list[0])
        self.optionmenu_parent_grade = tk.OptionMenu(self.new_window, self.get_parent_grade_choice, *parent_grade_list)
        self.optionmenu_parent_grade.pack()
        self.widget_list_new_window.append(self.optionmenu_parent_grade)

        self.submit_new_grade = tk.Button(self.new_window, text='Neue Note eintragen', command=self.submit)
        self.submit_new_grade.pack()
        self.widget_list_new_window.append(self.submit_new_grade)

    def submit(self):
        sql_insert_grade_into_grades = """INSERT INTO Grades (grade_name, grade_weight, course_id, child_of) VALUES(?, ?, ?, ?)"""
        grade_id_grade_name = self.get_parent_grade_choice.get()
        pos_of_delimiter = grade_id_grade_name.find(',')
        grade_id = grade_id_grade_name[0:pos_of_delimiter]
        sql_params = ('Neue Note', 0.2, self.Course_obj.Get_CourseID(), grade_id)
        self.db_connection.addToDatabase(sql_insert_grade_into_grades, sql_params)

        # remove the buttons and optionMenu from screen
        self.optionmenu_parent_grade.pack_forget()
        self.submit_new_grade.pack_forget()

        # plot the new pie
        self.plot_pie(self.zoom_slider.get())

        # update courseInfo Frame
        self.courseinfo_obj.Clear_CourseInfo()
        self.courseinfo_obj.GET_CourseInfo()
        self.new_window.destroy()

    def on_click(self, event):
        # screen position at which was clicked
        x_pos_of_clicking = event.mouseevent.x
        y_pos_of_clicking = event.mouseevent.y

        self.remove_widget_from_screen(self.widgets_in_canvas)

        self.edited_weight = tk.StringVar()
        self.edited_grade_name = tk.StringVar()
        self.edited_parent_grade_name = tk.StringVar()
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
                self.edit_grade_name = tk.Entry(self.canvas.get_tk_widget(), textvariable=self.edited_grade_name)
                self.widgets_in_canvas.append(self.edit_grade_name)
                self.edit_grade_name.place(x=x_pos_of_clicking, y=500-y_pos_of_clicking)
                self.Weight_pos = i

                def func(event):
                    self.update_grade_name(event, self.child_name_tuple, self.edited_grade_name, self.edit_grade_name)
                self.edit_grade_name.bind('<KeyPress>', func)

        for i, text in enumerate(self.outer_wedges_names):
            if event.artist == text:
                self.edited_parent_grade_name.set(self.parent_names_only[i])
                self.edit_grade_name = tk.Entry(self.canvas.get_tk_widget(), textvariable=self.edited_parent_grade_name)
                self.widgets_in_canvas.append(self.edit_grade_name)
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
                    if isinstance(widget, tk.Entry):
                        widget.pack_forget()

                self.edited_weight.set(str(self.child_weight_tuple[i]))
                self.entry_field_new_wedge = tk.Entry(self.canvas.get_tk_widget(), textvariable=self.edited_weight)
                self.widgets_in_canvas.append(self.entry_field_new_wedge)

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
                    if isinstance(widget, tk.Entry):
                        widget.pack_forget()
                self.edited_weight.set(str(self.parent_grade_weight_tuple[i]))
                self.entry_field_new_wedge = tk.Entry(self.canvas.get_tk_widget(), textvariable=self.edited_weight)
                self.widgets_in_canvas.append(self.entry_field_new_wedge)
                self.entry_field_new_wedge.place(x=x_pos_of_clicking, y=500-y_pos_of_clicking)

                pos_of_delimiter = self.parent_grade_name_tuple[i].find(',')
                self.grade_id = self.parent_grade_name_tuple[i][0:pos_of_delimiter]

                self.del_parent_grade_button = tk.Button(self.canvas.get_tk_widget(), text='Löschen', command=self.del_from_db)
                self.widgets_in_canvas.append(self.del_parent_grade_button)

                self.del_parent_grade_button.place(x=x_pos_of_clicking, y=500-y_pos_of_clicking-self.entry_field_new_wedge.winfo_height()-15)
                self.Weight_pos = i

                def func(event):
                    self.entry_input_handler(event, 2)

                self.entry_field_new_wedge.bind('<KeyPress>', func)

    def del_from_db(self):
        if int(self.grade_id) in self.dict_parents_and_childs.keys():
            for grade in self.dict_parents_and_childs[int(self.grade_id)]:
                sql_del_grade_child = "DELETE FROM Grades WHERE grade_id = ?"
                self.db_connection.addToDatabase(sql_del_grade_child, (grade[0],))

        sql_del_grade = "DELETE FROM Grades WHERE grade_id = ?"
        self.db_connection.addToDatabase(sql_del_grade, (self.grade_id, ))
        self.plot_pie(self.zoom_slider.get())
        self.remove_widget_from_screen(self.widgets_in_canvas)



    def entry_input_handler(self, event, update_pos):
        # Weight_pos is the Position of the edit weight:
        i = self.Weight_pos
        if update_pos == 1:
            self.WeightData = self.child_weight_tuple
            weight_names = self.child_name_tuple
        else:
            self.WeightData = self.parent_grade_weight_tuple
            weight_names = self.parent_grade_name_tuple
        if event.keysym == 'Return':
            edited_weight = float(self.edited_weight.get())
            if isinstance(edited_weight, float):
                pos_of_delimiter = weight_names[i].find(',')
                grade_id = weight_names[i][0:pos_of_delimiter]
                sql_update_grade_weight = "UPDATE Grades SET grade_weight = ? WHERE grade_id = ?"
                params_for_update = (edited_weight, int(grade_id))
                self.db_connection.addToDatabase(sql_update_grade_weight, params_for_update)
                self.plot_pie(self.zoom_slider.get())
                # update courseInfo Frame
                self.courseinfo_obj.Clear_CourseInfo()
                self.courseinfo_obj.GET_CourseInfo()
            self.entry_field_new_wedge.destroy()

    def update_grade_name(self, event, list_of_grade_names, var_entry_field, entry_field):
        if event.keysym == 'Return':
            new_grade_name = var_entry_field.get()
            sql_update_grade_name = "UPDATE Grades SET grade_name = ? WHERE grade_id = ?"
            grade_id_pos = list_of_grade_names[self.Weight_pos].find(',')
            grade_id = list_of_grade_names[self.Weight_pos][0:grade_id_pos]
            params = (new_grade_name, int(grade_id))
            self.db_connection.addToDatabase(sql_update_grade_name, params)
            entry_field.destroy()
            self.plot_pie()
            # update courseInfo Frame
            self.courseinfo_obj.Clear_CourseInfo()
            self.courseinfo_obj.GET_CourseInfo()


    def drag_pies(self, event):
        # store the location of the button press:
        #pdb.set_trace()
        self.press = event.x, event.y

    def on_motion(self, event):

        if self.press is None:
            return
        x0, y0 = self.press
        dx = event.x - x0
        dy = event.y - y0
        self.plot_pie(self.zoom_slider.get(), dx, dy)

    def on_release(self, event):
        self.press = None

    def init_event_handlers(self):
        self.press = None
        self.fig.canvas.mpl_connect('pick_event', lambda event: self.on_click(event))
        self.canvas.mpl_connect('button_press_event', self.drag_pies)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas.mpl_connect('button_release_event', self.on_release)

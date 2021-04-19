import tkinter as tk
import tkinter.ttk as ttk

#from CourseInfo import CourseInfo

import pdb


class read_mode:

    def __init__(self, frame):
        self.frame = frame
        self.treeview = ttk.Treeview(self.frame)
    #     pass

    def build_treeview(self, stud_grade_data):

        treeview = self.treeview
        treeview['columns'] = tuple(stud_grade_data.keys())
        treeview.column('#0', width=0, stretch=tk.NO)
        for heading in stud_grade_data.keys():

            treeview.column(heading, anchor=tk.CENTER)
            treeview.heading(heading, text=heading, anchor=tk.CENTER)
        if len(stud_grade_data.keys()) > 0:
            rows = len(stud_grade_data[tuple(stud_grade_data.keys())[0]])
        else:

            rows = 0

        list_of_list = []
        row_list = []
        row_data = []
        for i in range(0, rows):
            for key, value in stud_grade_data.items():
                try:
                    row_data.append(value[i])
                except:
                    print('Übergebene Listen waren inkonsistent!')
                    return 0
            list_of_list.append(tuple(row_data))
            row_data = []

        for i, row in enumerate(list_of_list):
            treeview.insert(parent='', index=i, iid=i, text='', values=row)

        #treeview.pack()
        self.treeview = treeview
        return self.treeview

    def show(self):
        if self.treeview.winfo_ismapped() == 0:
            self.treeview.pack()
            return self.treeview

    def hide(self):
        if self.treeview.winfo_ismapped() == 1:
            self.treeview.pack_forget()

import numpy as np
import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk
import re as re

from DB_con import *
from PieChart import *
from interact_with_excel import excel_interact
from CoursesDropdown_menu import CoursesDropdown_menu
from Calender import Calender
import pdb

def get_display_size():
    root = tk.Tk()
    root.update_idletasks()
    root.attributes('-fullscreen', True)
    root.state('iconic')
    height = root.winfo_screenheight()
    width = root.winfo_screenwidth()
    root.destroy()
    return (width, height)


def ManageCourses(db_connection, root):

    # get screen size:
    current_display_size = get_display_size()

    root1 = tk.Toplevel(root)
    style = ttk.Style(root1)
    style.configure("My.TLabel", font=('Arial', 25))

    parent_frame_courseInfo_window = tk.Frame(root1)
    parent_frame_courseInfo_window.grid(column=0, row=0, padx=20, pady=20)

    # Initalise the Frames which split the Window

    # the course info frame and the grade_edit frame need to be in one row
    # so the begining of the student_edit frame is not dependend on the second column
    Frame_courseInfo_grades_edit = tk.Frame(parent_frame_courseInfo_window, width=current_display_size[0]/2-20)
    Frame_courseInfo_grades_edit.grid(column=0, row=0, sticky='n')

    DropdownMenuFrame = tk.Frame(Frame_courseInfo_grades_edit, borderwidth=1, bd=1, relief=tk.SUNKEN)
    DropdownMenuFrame.grid(column=0, row=0)

    # the calender and the pie graph get also an addiational frame in which they are packed
    calender_pie_graph_frame = tk.Frame(parent_frame_courseInfo_window, width=current_display_size[0]/2-20)
    calender_pie_graph_frame.grid(column=1, row=0)

    calender_frame = tk.Frame(calender_pie_graph_frame, bd=1, relief=tk.SUNKEN, width=current_display_size[0]/2-20)
    calender_frame.grid(column=0, row=0)

    # second_frame = tk.Frame(root1)
    # second_frame.grid(column=0, row=1)
    CourseInfoFrame = tk.Frame(Frame_courseInfo_grades_edit, width=current_display_size[0]/2-20, height=500, bd=1, relief=tk.SUNKEN)
    CourseInfoFrame.grid(column=0, row=1)

    PieFrame = tk.Frame(calender_pie_graph_frame, bd=1, relief=tk.SUNKEN)
    #AddParticipantFrame = tk.Frame(root1, bd=1, relief=tk.SUNKEN)

    # Draw the Frames:
    PieFrame.grid(column=0, row=1)
    #AddParticipantFrame.grid(column=0, row=2)

    # the frame objects are stored in a list and given to the other classes
    #FrameList = [DropdownMenuFrame, CourseInfoFrame, PieFrame, AddParticipantFrame]

    FrameList = [parent_frame_courseInfo_window, DropdownMenuFrame, CourseInfoFrame, PieFrame, calender_frame]


    DropDownMenu = CoursesDropdown_menu(db_connection, FrameList, root1, current_display_size)
    DropDownMenu.init_tk_widgets()
    Calender_obj = Calender(db_connection, calender_frame, root1)
    Calender_obj.build_grid(2021, 4)
    root1.mainloop()

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


    # Initalise the Frames which split the Window
    DropdownMenuFrame = tk.Frame(root1, borderwidth=1, bd=1, relief=tk.SUNKEN, width=current_display_size[0]/2)
    DropdownMenuFrame.grid(column=0, row=0, sticky='nw')

    calender_frame = tk.Frame(root1, bd=1, relief=tk.SUNKEN, width=current_display_size[0]/2)
    calender_frame.grid(column=1, row=0)

    # second_frame = tk.Frame(root1)
    # second_frame.grid(column=0, row=1)
    CourseInfoFrame = tk.Frame(root1, width=current_display_size[0]/2, height=500, bd=1, relief=tk.SUNKEN)
    CourseInfoFrame.grid(column=0, row=1, sticky='nw')

    PieFrame = tk.Frame(root1, bd=1, relief=tk.SUNKEN)
    AddParticipantFrame = tk.Frame(root1, bd=1, relief=tk.SUNKEN)

    # Draw the Frames:
    PieFrame.grid(column=1, row=1)
    AddParticipantFrame.grid(column=0, row=2)

    # the frame objects are stored in a list and given to the other classes
    #FrameList = [DropdownMenuFrame, CourseInfoFrame, PieFrame, AddParticipantFrame]

    FrameList = [DropdownMenuFrame, CourseInfoFrame, PieFrame, AddParticipantFrame, calender_frame]


    DropDownMenu = CoursesDropdown_menu(db_connection, FrameList, root1, current_display_size)
    Calender_obj = Calender(db_connection, calender_frame, root1)
    Calender_obj.build_grid(2021, 4)
    root1.mainloop()

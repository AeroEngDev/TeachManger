from tkinter import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


def add_grade(db_connection):
    widget_add_grade = Toplevel()

    #  Get Available Courses:
    sql = f"""SELECT * FROM Courses"""
    #params = (, )
    Courses_list = db_connection.GetFromDatabase(sql, ())
    CourseNames_list = []
    for Courses in Courses_list:
        CoursesNames_list.append(Courses[0])

    # Create Dropdown-Widget with the CorseNames
    if len(CourseNames_list) > 0:
        clicked = StringVar()
        clicked.set(CourseNames_list[0])
        widget_dropdown_CourseNames = OptionMenu(widget_add_grade, clicked, *CourseNames_list)
        widget_dropdown_CourseNames.pack()
    else:
        widget_dropdown_CourseNames = OptionMenu(widget_add_grade, clicked, [])

    OpenCourse_Button = Button(widget_add_grade, text='Kurs öffnen', command=LoadCourse_Info)
    OpenCourse_Button.pack()



    # prepair the columns inside the frame
    Course_info_student_label = Label(Course_info_frame, column=0).pack()



    widget_add_grade.mainloop()


def LoadCourse_Info():
    Course_selected = clicked.get()

    sql_GET_gradeCount = f"""SELECT GradeStruct.gradeCount FROM GradeStruct WHERE GradeStruct.CourseID IN(SELECT Courses.CourseID FROM Courses WHERE CourseName=?)"""
    params = (Course_selected,)
    gradeCount = db_connection.GetFromDatabase(sql, params)
    gradeNames_list = []
    gradeWeightNames_list = []
    sql_GET_grades = f"""SELECT Students.forename, Students.surname, {Course_selected}.grade1,"""
    string_GradeStruct = 'grade1_weight'
    for i in range(2, gradeCount):
        gradeNames_list.append('grade'+str(i))
        gradeWeightNames_list.append('grade'+str(i)+'_weight')
        # Construct Query to get all grades in Course Course_selected
        sql_GET_grades = sql_GET_grades + f""", {Course_selected}.grade{i}"""
        # Construct String for GradeStruct
        string_GradeStruct = string_GradeStruct+f", grade{i}_weight"

    sql_GET_grades = sql_GET_grades+f""" FROM {Course_selected} INNER JOINS {Course_selected} ON students.id = {Course_selected}.StudentID """
    Selected_Course_NamesGrades_list = db_connection.GetFromDatabase(sql_GET_grades, ())

    # Get the Grade Structure
    sql_GET_gradeStruct = f"""SELECT {string_GradeStruct} FROM GradeStruct WHERE CourseID IN (SELECT Courses.CourseID FROM Courses WHERE Courses.CourseName = {Course_selected})"""

    GET_GradeStruct = db_connection.GetFromDatabase(sql_GET_gradeStruct, ())

    # die Rückgabe der Queries soll schön verarbeitet dargestellt werden.
    # dafür soll eine Tabelle mit Formularelementen dynamisch erzeugt werden, abhängig von
    # der Größe des Datensatzes:
    Course_info_frame = LabelFrame(widget_add_grade, text=f'Inhalt im aktuell ausgewählten Kurs {clicked.get()}').pack(padx=10, pady=10)
    i = 0
    j = 0
    for DataSet in Selected_Course_NamesGrades_list:
        for Entry in DataSet:
            Entry(Course_info_frame, text=Entry).grid(column=i, row=j)
            j = j + 1
        i = i + 1

    Course_Grade_Struct_Info = LabelFrame(widget_add_grade, text=f"Visualisierung der Notengewichtung:").pack()


    # sql = f"""SELECT Students.forname, Students.surname,  FROM {Course_choice}"""
    # Course_Info_selected = db_connection.GetFromDatabase(sql, ())
    #
    # studentID_list = []
    # for Info_selected in Course_Info_selected:
    #     studentID_list.append(Info_selected[1])

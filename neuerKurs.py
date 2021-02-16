import sqlite3
from DB_con import DB_con
import pdb


class Course:

    def __init__(self, db_conn, CourseName, Year, Contact_Name, Notes, CourseID):
        self.CourseID = CourseID
        self.CourseName = CourseName
        self.Year = Year
        #self.StudentNames = StudentNames
        # self. StudentGrades = StudentGrades
        # self.GradesStruct = GradesStruct
        self.Contact_Name = Contact_Name
        self.Notes = Notes
        StudentNames = []
        self.StudentNames = StudentNames

        ## erstelle eine Instanz von DB_conn()
        #db_conn = DB_con()
        self.db_conn = db_conn
        self.db_conn.CreateTableAllCourses()

        if self.CourseID != -1:
            sql = f"SELECT CourseID FROM Courses WHERE CourseName = ? AND Year = ? AND ContactName = ? AND Notes = ?"
            params = (self.CourseName, self.Year, self.Contact_Name, self.Notes)
            #pdb.set_trace()
            if len(self.db_conn.GetFromDatabase(sql, params)) == 0:
                #pdb.set_trace()
                ## Trage den Kurs in die Tabelle Courses ein. In dieser Tabelle sind alle Kurse enthalten
                sql = "INSERT INTO Courses (CourseID, CourseName, Year, ContactName, Notes) VALUES (Null, ?, ?, ?, ?)"
                params = (self.CourseName, self.Year, self.Contact_Name, self.Notes)
                db_conn.addToDatabase(sql, params)

                ## Bestimme die zugewiesene ID des Kurses
                sql = "SELECT CourseID FROM Courses WHERE CourseName = ? AND Year = ? AND ContactName = ? AND Notes = ?"
                Ausgabe = db_conn.GetFromDatabase(sql, params)
                CourseID = Ausgabe[0]
                db_conn.CreateTableSingleCourse(self.CourseName, CourseID)
            else:
                print(f'Kurs {CourseName} ist schon vorhanden!')
        else:
            pass
        # self.conn = sqlite3.connect("database.db")
        # self.c = self.conn.cursor()
        #self.StudentNames = []

        # Initalise Connection to the Database
        # If the File doesnt exists, it will be created

    # def __del__(self):
    #     del self.db_conn

    def Get_CourseID(self):
        self.db_conn = DB_con()
        sql = f"SELECT CourseID FROM Courses WHERE CourseName = ? AND Year = ? AND ContactName = ?"
        params = (self.CourseName, self.Year, self.Contact_Name)
        CourseID_list = self.db_conn.GetFromDatabase(sql, params)
        return CourseID_list[0][0]

    def AddStudent(self, studentID):
        self.db_conn = DB_con()
        # Überprüfe, ob Studierender schon vorhanden ist:
        sql = f"SELECT StudentID FROM [{self.CourseName}] WHERE StudentID = ?"
        results_studentID = self.db_conn.GetFromDatabase(sql, studentID)
        if len(results_studentID) == 0:
            sql = f"INSERT INTO [{self.CourseName}] (StudentID) VALUES (?)"
            self.db_conn.addToDatabase(sql, studentID)
        else:
            print('Student ist schon in diesem Kurs eingetragen!')
        # self.c.execute(sql, params)
        # self.conn.commit()

        #self.StudentNames.append(student)
        #print(student)

    def addGradeColumn(self, GradeName, GradeWeight, CourseID):
        self.db_conn = DB_con()
        sql = f"PRAGMA table_info([{self.CourseName}]);"
        Column_list = self.db_conn.GetFromDatabase(sql, ())
        ColumnName_List = []
        for Tupel in Column_list:
            ColumnName_List.append(Tupel[1])
        if GradeName not in ColumnName_List:
            sql = f"ALTER TABLE [{self.CourseName}] ADD COLUMN [{GradeName}] INTEGER"
            self.db_conn.addToDatabase(sql, ())

            sql = f"ALTER TABLE [Struct {self.CourseName}] ADD COLUMN  [{GradeName}] REAL"
            self.db_conn.addToDatabase(sql, ())
            sql = f"UPDATE [Struct {self.CourseName}] SET ([{GradeName}]) = ? WHERE CourseID = ?"
            params = (GradeWeight, CourseID)
            self.db_conn.addToDatabase(sql, params)
        else:
            print(f'Die Spalte mit dem Notennamen {GradeName} ist bereits vorhanden!')

    # def close_DB(self):
    #     del self.db_conn

    def RemoveGradeColumn(self, ColumnName):
    # to delete a Column, a new table must be created and the data must be copied except the column, which should be deleted
        pass

    def addGrade(self, studentID, grade, GradeColumns):
        self.db_conn = DB_con()
        if isinstance(grade, dict):
            # sql = f"PRAGMA  table_info([{self.CourseName}]);"
            # DB_table_answer = self.db_conn.GetFromDatabase(sql, ())
            #self.c.execute(sql)
            # DB_table_answer = self.c.fetchall()
            for grade_obj in grade:
                key =grade_obj
                element = grade[grade_obj]
                if key in GradeColumns:
                    params = (element, studentID[0])
                    sql = f"UPDATE [{self.CourseName}] SET [{key}] = ? WHERE StudentID = ?"
                    self.db_conn.addToDatabase(sql, params)
                    # self.c.execute(sql, params)
                    # self.conn.commit()
        else:
            print('Fehler! Die Noten konnten nicht eingetragen werden!')

    def ShowGrade(self, StudentID, Column_Names, GradeColumnsString):
        self.db_conn = DB_con()
        sql = f"SELECT {GradeColumnsString} FROM [{self.CourseName}] WHERE StudentID = ?"
        gradeValues = self.db_conn.GetFromDatabase(sql, StudentID)
        dict_NamesGrades = {}
        gradeValues_tupel = gradeValues[0]
        i = 0
        for i in range(len(Column_Names)):
            dict_NamesGrades.update({Column_Names[i]: gradeValues_tupel[i]})
        return dict_NamesGrades


    def RmStudent(self, StudentID):
        self.db_conn = DB_con()
        # self.StudentNames.remove(student)
        sql = f"DELETE FROM [{self.CourseName}] WHERE StudentID = ?"
        params = StudentID
        self.db_conn.addToDatabase(sql, params)
        #print('Hier muss auf die Tabelle Studenten zugegriffen werden, und ein Student gelöscht werden!')

    def ShowStudents(self):
        self.db_conn = DB_con()
        sql_select_id = f"SELECT StudentID FROM {self.CourseName}"
        studentID_list = self.db_conn.GetFromDatabase(sql_select_id, None)
        # self.c.execute(sql_select_id)
        # studentID_list = self.c.fetchall()
        student_data = []
        for studentID in studentID_list:
            sql_select_names = f"SELECT (forname, surname, SchoolYear) FROM Students WHERE ID = ?"
            params = (studentID, )

            #self.c.execute(sql_select_names, params)
            student_data.append(self.db_conn.GetFromDatabase(sql_select_names, params))

        return student_data

    def ResultingGrade(self, StudentID, GradeColumns, GradeColumnsString):
        ## Get Grades for StudentID
        self.db_conn = DB_con()
        sql = f"SELECT {GradeColumnsString} FROM [{self.CourseName}] WHERE StudentID = ?"
        params = StudentID
        grade_tuple_list = self.db_conn.GetFromDatabase(sql, params)
        grade_tuple = grade_tuple_list[0]

        ## Get Grade Weights
        sql = f"SELECT {GradeColumnsString} FROM [Struct {self.CourseName}]"
        params = ()
        gradeStruct_list = self.db_conn.GetFromDatabase(sql, params)
        gradeStruct = gradeStruct_list[0]
        i = 0
        sum = 0
        for i in range(len(grade_tuple)):
            sum += gradeStruct[i]*grade_tuple[i]
        return sum
        # grade_dict_Weights = {}
        # for gradeStruct_Array in gradeStruct_list:
        #     if gradeStruct_Array[0] != None:
        #         grade_dict_Weights.update({gradeStruct_Array[0]:  gradeStruct_Array[1]})
        # i = 0
        # dict_Grades = {}
        # for i in range(len(GradeColumns)):
        #     if grade_tupel[0][i] != None:
        #         dict_Grades.update({GradeColumns[i]: grade_tupel[0][i]})
        # sum = 0
        # try:
        #     for GradeName, Grade in dict_Grades:
        #         sum += Grade*grade_dict_Weights[GradeName]
        #     return sum
        # except:
        #     print('Noten sind fehlerhaft eingetragen. Es konnte keine Note berechnet werden!')
        #     return 0

    def Get_GradeColumns(self):
        self.db_conn = DB_con()
        sql = f"PRAGMA  table_info([{self.CourseName}]);"
        params = ()
        Column_information =  self.db_conn.GetFromDatabase(sql, params)
        Column_Names = []
        for column in Column_information:
            Column_Names.append(column[1])
        Column_Names.remove('id')
        Column_Names.remove('StudentID')
        #Column_Names.remove('GradeStruct')
        Column_Names.remove('Notes')
        GradeColumnsString = ''
        for GradeName in Column_Names:
            if GradeColumnsString == '':
                GradeColumnsString = f"[{GradeName}]"
            else:
                GradeColumnsString = GradeColumnsString + f",[{GradeName}]"
        return Column_Names, GradeColumnsString

    def Get_CourseName(self):
        #self.db_conn = DB_con()
        return self.CourseName

    def ShowTable(self):
        #self.db_conn = DB_con()
        return self.db_conn.ShowTable(self.CourseName)

class Student:

    def __init__(self, forname, surname, SchoolYear, Tutor):
        self.forname = forname
        self.surname = surname
        self.SchoolYear = SchoolYear
        self.Tutor = Tutor

        self.db_conn = DB_con()
        self.db_conn.CreateStudentsTable()
        # self.conn = sqlite3.connect("database.db")
        # self.c = self.conn.cursor()

    def ShowStudent(self):
        ausgabe = (self.forname, self.surname, self.SchoolYear)
        return ausgabe
    def AddStudent(self):
        sql = "SELECT forname, surname, SchoolYear FROM Students WHERE forname = ? AND surname = ? AND SchoolYear = ? AND Tutor = ?"
        params = (self.forname, self.surname, self.SchoolYear, self.Tutor)
        Ausgabe = self.db_conn.GetFromDatabase(sql, params)
        if len(Ausgabe) == 0:
            sql = "INSERT INTO Students VALUES (NULL, ?, ?, ?, ?)"
            self.db_conn.addToDatabase(sql, params)
            # self.c.execute(sql, params)
            # self.conn.commit()
        else:
            print('Student ist schon im System vorhanden!')

    def Get_ID(self):
       sql = "SELECT ID FROM Students WHERE forname = ? AND surname = ? AND SchoolYear = ?"
       params = (self.forname, self.surname, self.SchoolYear)
       ausgabe = self.db_conn.GetFromDatabase(sql, params)
       #self.c.execute(sql, params)
       studentID = ausgabe[0]
       return studentID

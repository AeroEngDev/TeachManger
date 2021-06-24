
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

        sql = f"SELECT course_id FROM Courses WHERE course_name = ? AND year = ? AND contact_name = ? AND notes = ?"
        params = (self.CourseName, self.Year, self.Contact_Name, self.Notes)
        #pdb.set_trace()
        if len(self.db_conn.GetFromDatabase(sql, params)) == 0:
            #pdb.set_trace()
            ## Trage den Kurs in die Tabelle Courses ein. In dieser Tabelle sind alle Kurse enthalten
            sql = "INSERT INTO Courses (course_id, course_name, year, contact_name, notes) VALUES (Null, ?, ?, ?, ?)"
            params = (self.CourseName, self.Year, self.Contact_Name, self.Notes)
            db_conn.addToDatabase(sql, params)

            ## Bestimme die zugewiesene ID des Kurses
            sql = "SELECT course_id FROM Courses WHERE course_name = ? AND year = ? AND contact_name = ? AND notes = ?"
            Ausgabe = db_conn.GetFromDatabase(sql, params)
            self.CourseID = Ausgabe[0][0]
        else:
            print(f'Kurs {CourseName} ist schon vorhanden!')

        # self.conn = sqlite3.connect("database.db")
        # self.c = self.conn.cursor()
        #self.StudentNames = []

        # Initalise Connection to the Database
        # If the File doesnt exists, it will be created

    # def __del__(self):
    #     del self.db_conn
    def GET_gradeNames(self):
        sql = "SELECT gradeNames.grade1_Name"
        for i in range(2, self.GET_gradeCount()+1):
            sql = sql+f", gradeNames.grade{i}_Name"

        sql = sql + " FROM gradeNames, Courses WHERE gradeNames.CourseID IN(SELECT Courses.CourseID WHERE Courses.CourseName = ? AND Courses.Year = ? AND Courses.ContactName = ? AND Courses.Notes = ?)"
        params = (self.CourseName, self.Year, self.Contact_Name, self.Notes)
        gradeNames_list = self.db_conn.GetFromDatabase(sql, params)
        #pdb.set_trace()
        return gradeNames_list[0]

    def GET_gradeCount(self):
        sql = "SELECT gradeStruct.gradeCount FROM gradeStruct, Courses WHERE gradeStruct.CourseID IN(SELECT Courses.CourseID WHERE Courses.CourseName = ? AND Courses.Year = ? AND Courses.ContactName = ? AND Courses.Notes = ?)"
        params = (self.CourseName, self.Year, self.Contact_Name, self.Notes)
        gradeCount_list = self.db_conn.GetFromDatabase(sql, params)
        return gradeCount_list[0][0]
    def GET_CourseName(self):
        return self.CourseName

    def InsertIntoGradeStruct(self):
        #sql_get_CourseID = f"SELECT CourseID FROM Courses WHERE "

        sql_INSERT_gradeStruct = f"INSERT INTO gradeStruct (CourseID, gradeCount, grade1_weight, grade2_weight) VALUES (?, ?, ?, ?)"
        params = (self.CourseID, 2, 0.333, 0.666)
        self.db_conn.addToDatabase(sql_INSERT_gradeStruct, params)
        sql_INSERT_gradeNames = "INSERT INTO gradeNames (CourseID, grade1_Name, grade2_Name) VALUES (?, ?, ?)"
        params = (self.CourseID, 'Allgemeiner Teil', 'Schriftlich')
        self.db_conn.addToDatabase(sql_INSERT_gradeNames, params)

    def Get_CourseID(self):
        #self.db_conn = DB_con()
        sql = f"SELECT course_id FROM Courses WHERE course_name = ? AND year = ? AND contact_name = ?"
        params = (self.CourseName, self.Year, self.Contact_Name)
        CourseID_list = self.db_conn.GetFromDatabase(sql, params)
        return CourseID_list[0][0]

    def AddStudent(self, studentID):
        #self.db_conn = DB_con()
        # Überprüfe, ob Studierender schon vorhanden ist:
        sql = f"SELECT student_id FROM [{self.CourseName}] WHERE student_id = ?"
        #pdb.set_trace()
        results_studentID = self.db_conn.GetFromDatabase(sql, (studentID,))
        #pdb.set_trace()
        if len(results_studentID) == 0:
            sql = f"INSERT INTO [{self.Get_CourseID()}] (student_id) VALUES (?)"
            self.db_conn.addToDatabase(sql, (studentID,))
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
        #self.db_conn = DB_con()
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
        #self.db_conn = DB_con()
        sql = f"SELECT {GradeColumnsString} FROM [{self.CourseName}] WHERE StudentID = ?"
        gradeValues = self.db_conn.GetFromDatabase(sql, StudentID)
        dict_NamesGrades = {}
        gradeValues_tupel = gradeValues[0]
        i = 0
        for i in range(len(Column_Names)):
            dict_NamesGrades.update({Column_Names[i]: gradeValues_tupel[i]})
        return dict_NamesGrades


    def RmStudent(self, StudentID):
        #self.db_conn = DB_con()
        # self.StudentNames.remove(student)
        sql = f"DELETE FROM [{self.CourseName}] WHERE StudentID = ?"
        params = StudentID
        self.db_conn.addToDatabase(sql, params)
        #print('Hier muss auf die Tabelle Studenten zugegriffen werden, und ein Student gelöscht werden!')

    def ShowStudents(self):
        #self.db_conn = DB_con()
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
        #self.db_conn = DB_con()
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

    def Get_GradeColumns(self):
        #self.db_conn = DB_con()
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

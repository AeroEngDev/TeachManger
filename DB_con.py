import sqlite3
import pdb


class DB_con:
    def __init__(self, db_name):
        try:
            self.conn = sqlite3.connect(db_name)
            self.c = self.conn.cursor()
        except:
            pass

    def __del__(self):
        self.conn.close()

    def CreateStudentsTable(self):

        sql_string = """CREATE TABLE IF NOT EXISTS Students
        (student_id INTEGER,
        forname STRING,
        surname STRING,
        school_year STRING,
        tutor STRING,
        PRIMARY KEY (student_id))"""
        self.c.execute(sql_string)

    def CreateTableAllCourses(self):
        sql_create_courses = """CREATE TABLE IF NOT EXISTS Courses
        (course_id INTEGER,
        course_name STRING,
        year STRING,
        contact_name STRING,
        notes STRING,
        PRIMARY KEY (course_id))"""

        # create the courses table: Details about the Courses are saved here
        self.c.execute(sql_create_courses)

        sql_create_grades_table = """CREATE TABLE IF NOT EXISTS Grades
        (grade_id INTEGER,
        course_id INTEGER,
        grade_Name STRING,
        grade_weight FLOAT,
        child_of INTEGER NOT NULL DEFAULT '1',
        PRIMARY KEY (grade_id),
        FOREIGN KEY(course_id) REFERENCES Courses(course_id))
        """

        self.c.execute(sql_create_grades_table)

        sql_create_junktion_table_stud_courses = """CREATE TABLE IF NOT EXISTS stud_courses
        (student_id INTEGER,
        course_id INTEGER,
        FOREIGN KEY(student_id) REFERENCES Students(student_id),
        FOREIGN KEY(course_id) REFERENCES Courses(course_id)
        )"""

        self.c.execute(sql_create_junktion_table_stud_courses)

        sql_create_junktion_table_stud_courses_grades = """CREATE TABLE IF NOT EXISTS stud_courses_grades
        (student_id INTEGER,
        course_id INTEGER,
        grade_id INTEGER,
        grade_value INTEGER,
        FOREIGN KEY(student_id) REFERENCES Students(student_id),
        FOREIGN KEY(course_id) REFERENCES Courses(course_id),
        FOREIGN KEY(grade_id) REFERENCES Grades(grade_id)
        )"""

        ## create the junktion table between students and courses
        self.c.execute(sql_create_junktion_table_stud_courses_grades)

        # create the grade struct table
        # self.c.execute("CREATE TABLE IF NOT EXISTS GradeStruct (CourseID INTEGER NOT NULL, gradeCount INTEGER NOT NULL DEFAULT '2', grade1_weight FLOAT DEFAULT '0.666', grade2_weight FLOAT DEFAULT '0.333')")
        # self.c.execute("CREATE TABLE IF NOT EXISTS GradeNames (CourseID INTEGER NOT NULL, grade1_Name STRING, grade2_Name STRING)")

    def CreateTableSingleCourse(self, course_id):
        pass
        # sql_string = f"""CREATE TABLE IF NOT EXISTS [{course_id}]
        # (student_id INTEGER,
        # grade_1_value INTEGER DEFAULT '',
        # grade_1_name STRING DEFAULT 'Neue Note',
        # grade_1_child_of STRING DEFAULT 'none',
        # grade_1_weight INTEGER DEFAULT '0.2',
        # grade_2_value INTEGER DEFAULT '',
        # grade_2_name STRING DEFAULT 'Neue Note',
        # grade_2_child_of STRING DEFAULT 'none',
        # grade_2_weight INTEGER DEFAULT '0.2',
        # Notes STRING,
        # FOREIGN KEY(student_id) REFERENCES Students(student_id)
        # )"""
        # pdb.set_trace()
        # self.c.execute(sql_string)
        #self.conn.commit()

    def CreateTableCalenderEntries(self):
        sql = """CREATE TABLE IF NOT EXISTS CalenderEntries (entry_id INTEGER, entry_name TEXT, date Date,
         notes TEXT, alert_timing TEXT, PRIMARY KEY(entry_id))"""
        self.c.execute(sql)

        sql_junktion_table = """CREATE TABLE IF NOT EXISTS cal_stud_courses
         (entry_id INTEGER,
         student_id INTEGER,
         course_id INTEGER,
         FOREIGN KEY(entry_id) REFERENCES CalenderEntries(entry_id),
         FOREIGN KEY(student_id) REFERENCES Students(student_id),
         FOREIGN KEY(course_id) REFERENCES Courses(course_id))"""
        self.c.execute(sql_junktion_table)

    def CreateTableSettings(self):

        sql = f"""CREATE TABLE IF NOT EXISTS Settings (SettingsID INTEGER, AlertTiming INTEGER, PRIMARY KEY(SettingsID))"""
        self.c.execute(sql)
    def addToDatabase(self, sql, params):

        self.c.execute(sql, params)
        self.conn.commit()

    def GetFromDatabase(self, sql, params):

        self.c.execute(sql, params)
        return self.c.fetchall()

    def ShowTable(self, tableName):
        sql = f"SELECT * FROM [{tableName}]"
        self.c.execute(sql, ())
        return self.c.fetchall()

    # it must be find out how many grades are given in one course
    # therefore a function is written, which looks inside the Course Table of the
    # wanted course and takes that information

    def GetGradeNumber(CourseName):
        # it has to be checked if this method is obsoled

        # it looks into CourseName and returns the number of grades inside the table
        sql = f"""SELECT FROM {CourseName} """

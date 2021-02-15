import sqlite3


class DB_con:
    def __init__(self):
        self.conn = sqlite3.connect("database.db")
        self.c = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def CreateStudentsTable(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS Students (id INTEGER, forname STRING, surname STRING, SchoolYear STRING, Tutor STRING, PRIMARY KEY (ID))")

    def CreateTableAllCourses(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS Courses (CourseID INTEGER, CourseName STRING, Year STRING, ContactName STRING, Notes STRING, PRIMARY KEY (CourseID))")

        # create the grade struct table
        self.c.execute("CREATE TABLE IF NOT EXISTS GradeStruct (CourseID INTEGER NOT NULL, gradeCount INTEGER NOT NULL DEFAULT '2', grade1_weight FLOAT, grade2_weight FLOAT)")

    def CreateTableSingleCourse(self, CourseName, CourseID):
        self.c.execute(f"CREATE TABLE IF NOT EXISTS [{CourseName}] (id INTEGER, StudentID INTEGER, Grade1 FLOAT DEFAULT '0.333', Grade2 FLOAT DEFAULT '0.666', Notes STRING, PRIMARY KEY (ID))")
        self.conn.commit()

    def CreateTableCalenderEntries(self):
        sql = f"""CREATE TABLE IF NOT EXISTS CalenderEntries (EntryID INTEGER, EntryName TEXT, EntryYear INTEGER,
        EntryMonth INTEGER, EntryDay INTEGER, EntryHour INTEGER,
        EntryMin INTEGER, Notes TEXT, LinkedPersons BLOB, AlertTiming TEXT, PRIMARY KEY(EntryID))"""
        self.c.execute(sql)

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

import sqlite3
from DB_con import DB_con
import pdb


class Student:

    def __init__(self, forname, surname, SchoolYear, Tutor, db_connection):

        self.forname = forname
        self.surname = surname
        self.SchoolYear = SchoolYear
        self.Tutor = Tutor
        self.db_conn = db_connection
        #self.db_conn = DB_con()
        self.db_conn.CreateStudentsTable()

        ## its better to check the id, than all the other entries!!

        sql = "SELECT forname, surname, school_year FROM Students WHERE forname = ? AND surname = ? AND school_year = ? AND tutor = ?"
        params = (self.forname, self.surname, self.SchoolYear, self.Tutor)
        Ausgabe = self.db_conn.GetFromDatabase(sql, params)
        if len(Ausgabe) == 0:
            sql = "INSERT INTO Students VALUES (NULL, ?, ?, ?, ?)"
            self.db_conn.addToDatabase(sql, params)
            # self.c.execute(sql, params)
            # self.conn.commit()
        else:
            print('Student ist schon im System vorhanden!')
        # self.conn = sqlite3.connect("database.db")
        # self.c = self.conn.cursor()

    def ShowStudent(self):
        ausgabe = (self.forname, self.surname, self.SchoolYear)
        return ausgabe

    def Get_ID(self):
       sql = "SELECT student_id FROM Students WHERE forname = ? AND surname = ? AND SchoolYear = ?"
       params = (self.forname, self.surname, self.SchoolYear)
       ausgabe = self.db_conn.GetFromDatabase(sql, params)
       #pdb.set_trace()
       #self.c.execute(sql, params)
       studentID = ausgabe[0][0]
       #pdb.set_trace()
       return studentID

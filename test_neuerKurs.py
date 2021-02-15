import unittest
from neuerKurs import *

class test_neuerKurs(unittest.TestCase):
    # def test_einzigartig(self):
    #     self.assertEqual(True, False)
    def test_createTable(self):
        Init_DB = DB_con()
        Init_DB.CreateStudentsTable()
        Init_DB.CreateTableAllCourses()
        del Init_DB
        # Init_DB.CreateTableGradeStruct()
        #Init_DB.CreateTableSingleCourse('', 123)
    def test_neuerKurs(self):
        Geo_Course = Kurs('Geografie 10a', '10', 'Hr. Müller', 'Klassenraum 304')
        Student_Tobi = Student('Martin Tobias', 'Degner', '9a')
        Student_Tobi.AddStudent()
        Student_ID = Student_Tobi.Get_ID()
        print(Student_Tobi.ShowStudent())
        Geo_Course.AddStudent(Student_ID)
    def test_AddGrade(self):
        Mathe_Course = Kurs('Mathe 7a', '7', 'Fr. Schneider', 'Ohrenstöpsel mitnehmen!')
        Student_Bill = Student('Bill', 'Richter', '7a')
        Student_Bill.AddStudent()
        Student_ID = Student_Bill.Get_ID()
        Mathe_Course.AddStudent(Student_ID)
        Mathe_Course.RmStudent(Student_ID)
        print(Mathe_Course.ShowTable())
        Mathe_Course.addGradeColumn('Mündlich Präsentation', 0.5, Mathe_Course.Get_CourseID())
        Mathe_Course.addGradeColumn('Mündlich AT', 0.25, Mathe_Course.Get_CourseID())
        Mathe_Course.addGradeColumn('Schriftlich Klausur', 0.25, Mathe_Course.Get_CourseID())
        dict_grades = {'Mündlich Präsentation': 7, 'Mündlich AT': 6, 'Schriftlich Klausur': 12}
        Mathe_Course.AddStudent(Student_ID)
        ColumnNames, ColumnNamesString = Mathe_Course.Get_GradeColumns()
        Mathe_Course.addGrade(Student_ID, dict_grades, ColumnNames)
        self.assertEqual(8, Mathe_Course.ResultingGrade(Student_ID, ColumnNames, ColumnNamesString))
        self.assertEqual(dict_grades, Mathe_Course.ShowGrade(Student_ID, ColumnNames, ColumnNamesString))
        #Mathe_Course.close_DB()
if __name__ == '__main__':
    unittest.main()

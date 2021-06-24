import unittest
import tkinter as tk
import tkinter.ttk as ttk
import pdb

from read_mode import read_mode


class Test_read_mode_class(unittest.TestCase):

    # def __init__(self):
    #     self.window = tk.Tk()

    # def read_stud_grade_in_course(self):
    #
    #     course_id = 1

    def test_build_treeview(self):
        window = tk.Tk()
        self.courseInfo_read_mode = read_mode(window)
        dict = {}
        treeview_widget = ttk.Treeview()
        self.assertEqual(self.courseInfo_read_mode.build_treeview(dict).winfo_children(), treeview_widget.winfo_children())

    def test_build_treeview_with_two_elements(self):
        window = tk.Tk()
        self.courseInfo_read_mode = read_mode(window)
        dict = {'ID': [1, 2], 'Vorname': ['Micha', 'Katrin']}
        treeview_widget = self.courseInfo_read_mode.build_treeview(dict)

        # check if the first column is ID:
        self.assertEqual(treeview_widget.cget('columns')[0], 'ID')
        # check if the second column is Vorname:
        self.assertEqual(treeview_widget.cget('columns')[1], 'Vorname')

        # check if row 1 is shown like it should:
        self.assertEqual(treeview_widget.item(0)['values'], [1, 'Micha'])

        # check if row 2 is shown like it should:
        self.assertEqual(treeview_widget.item(1)['values'], [2, 'Katrin'])

    def test_lists_are_inconsistent(self):
        window = tk.Tk()
        self.courseInfo_read_mode = read_mode(window)
        dict = {'ID': [1, 2, 3], 'Vorname': ['Micha', 'Katrin']}
        treeview_widget = self.courseInfo_read_mode.build_treeview(dict)
        self.assertEqual(treeview_widget, 0)

    def test_show(self):
        window = tk.Tk()
        self.courseInfo_read_mode = read_mode(window)
        dict = {'ID': [1, 2], 'Vorname': ['Micha', 'Katrin']}
        treeview_widget = self.courseInfo_read_mode.build_treeview(dict)
        treeview_widget.pack_forget()
        self.assertEqual(self.courseInfo_read_mode.show().winfo_ismapped(), 1)

if __name__ == '__main__':
    unittest.main()

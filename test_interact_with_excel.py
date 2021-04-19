import unittest
import os as os
from interact_with_excel import excel_interact

# 1.) write a failing test

# first test: create a empty excel spreatsheet:


class create_excel_sheet_test(unittest.TestCase):
    # def __init__(self):

    #
    # def test_create_empty_excel_sheet(self):
    #
    #     self.file_name = 'worksheet.xlsx'
    #     excel_sheet = excel_interact(self.file_name)
        # self.assertEqual(excel_sheet.create([], []), os.system(f"find {self.file_name}"))

    def test_create_excel_sheet_data_columns_same_length(self):
        self.file_name = 'worksheet.xlsx'
        # create dictionary with data in it
        # the columns have the same length
        data_list = []
        data_list.append(('Michael', 'Müller', 3, 2, 4, 5))
        data_list.append(('Tobias', 'Schneider', 5, 10, 11))
        data_list.append(('Barbara', 'Muster', 1, 15, 15, 14))

        dict_headings_list = []
        dict_headings_list = ['Mündlich 1', 'Mündlich 2', 'Mündlich 3', 'Schritlich1', 'Schriftlich 2']

        excel_sheet = excel_interact(self.file_name)
        file_name_of_created_sheet = excel_sheet.create(dict_headings_list, data_list)

        self.assertEqual(excel_sheet.read(), [dict_headings_list, data_list])



    # def test_create_excel_pie_chart(self):
    #
    #     # test creating a simple pie chart with excel:
    #     grade_weight_data = {}
    #     grade_weight_data['Mündlich'] = {'Vortrag': 0.1, 'Mitarbeit': 0.2}
    #     grade_weight_data['Schriftlich'] = {'Test 1': 0.2, 'Test 2': 0.1}
    #     grade_weight_data['Sozialverhalten'] = {'Ausflug': 0.4}
    #
    #     excel_sheet = excel_interact(self.file_name, {})
    #     file_name_of_created_sheet = excel_sheet.create()
    #
    #     self.assertEqual(excel_sheet.draw_pie_plot(grade_weight_data), excel_sheet.get_grade_weight_plot())

    #def test_

if __name__ == '__main__':
    unittest.main()

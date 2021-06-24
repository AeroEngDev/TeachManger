from interact_with_excel import excel_interact
import os


hallo = excel_interact('hallo.xlsx', {})
workbook = hallo.create()
grade_weight_data = {}
grade_weight_data['Mündlich'] = {'Vortrag': 0.1, 'Mitarbeit': 0.2}
grade_weight_data['Schriftlich'] = {'Test 1': 0.2, 'Test 2': 0.1}
grade_weight_data['Sozialverhalten'] = {'Ausflug': 0.4}
hallo.draw_pie_plot(workbook, grade_weight_data)
os.system('libreoffice hallo.xlsx')

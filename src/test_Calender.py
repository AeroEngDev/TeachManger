import unittest
import tkinter as tk
import tkinter.ttk as ttk
import pdb
import datetime as dt


from DB_con import DB_con


class test_Calender(unittest.TestCase):

    def test_make_cal_entry(self):
        db_connection = DB_con()

        # the new calender entry should be on may 20 at 12h
        entry_date = dt.datetime(2021, 5, 20, 12, 00)
        #pdb.set_trace()
        entry_name = "Klausur"
        entry_notes = "Raum 203"
        alertTiming = "1d"

        # sql_add_to_db = "INSERT INTO CalenderEntries (entry_name, date, notes, alert_timing) VALUES (?, ?, ? , ?)"
        params = (entry_name, entry_date, entry_notes, alertTiming)
        # db_connection.addToDatabase(sql_add_to_db, params)

        # read out the entity and check if the data is saved the right way:
        sql_select_statement = "SELECT entry_name, date, notes, alert_timing FROM CalenderEntries WHERE entry_name = ? AND date = ? AND notes = ? AND alert_timing = ?"
        db_output = db_connection.GetFromDatabase(sql_select_statement, params)
        output = db_output[0]
        #pdb.set_trace()
        self.assertEqual(output[0], "Klausur")
        self.assertEqual(output[1], dt.datetime(2021, 5, 20, 12, 00).strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(output[2], "Raum 203")
        self.assertEqual(output[3], "1d")


if __name__ == '__main__':
    unittest.main()

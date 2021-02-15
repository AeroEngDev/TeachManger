import unittest
import datetime
import numpy as np
from Calender import calender

class MyTestCase(unittest.TestCase):
    def test_calenderEntry(self):
        self.init_cal = calender()

        ## heute in 7 Tagen
        tday_datetime = datetime.datetime.now()
        event_datetime_klausur = datetime.datetime(2021, 1, 21, 12, 0)
        tdelta_event_klausur = datetime.timedelta(days=5)
        #event_alert_klausur = datetime.datetime(2021, 1, 21, 7, 0)
        print(event_datetime_klausur)

        # die Funktion sollte False zurückgeben, weil nach der ersten Ausführung des Tests eine Eintragung nicht mehr stattfinden soll!
        self.assertEqual(False, self.init_cal.new_entry(event_datetime_klausur, 'Klausur Geografie', 'Schmierpapier mitnehmen!', 'Klasse 7a', tdelta_event_klausur))
        print(self.init_cal.check_for_alert())
        del self.init_cal
    def test_do_alert(self):
        self.init_cal = calender()
        event_einkaufen = datetime.datetime(2021, 1, 16, 23, 0)
        tdelta = datetime.timedelta(hours=1)
        self.assertEqual(False, self.init_cal.new_entry(event_einkaufen, 'Einkaufen mit Mama', 'Schlüssel mitnehmen', 'Lis', tdelta))
        print(self.init_cal.check_for_alert())
    def test_show_calender(self):
        self.init_cal = calender()
        self.init_cal.ShowCalender(2021, 1)
if __name__ == '__main__':
    unittest.main()

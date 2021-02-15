import datetime
import sqlite3
import numpy as np
from DB_con import DB_con


class calender:
    def __init__(self):
        self.db_conn = DB_con()
        #self.db_conn = db_conn
        self.db_conn.CreateTableCalenderEntries()

    def new_entry(self, EntryDate, EntryName, Notes, LinkedPersons, AlertTiming):
        ## Umrechnung des Alert-Timings in ein Datum:
        datum_alert_timing = EntryDate - AlertTiming
        datum_alert_timing_str = datetime.datetime.strftime(datum_alert_timing, '%d.%m.%Y %H:%M:%S')

        entry_date_year = EntryDate.year
        entry_date_month = EntryDate.month
        entry_date_day = EntryDate.day
        entry_date_hour = EntryDate.hour
        entry_date_minute = EntryDate.minute

        # EntryDate_Str = datetime.datetime.strftime(EntryDate, '%d.%m.%Y %H:%M:%S')

        # Überprüfen, ob der Eintrag schon existiert:
        sql = f"""SELECT EntryName, EntryYear, EntryMonth, EntryDay, EntryHour, EntryMin, Notes, LinkedPersons, AlertTiming FROM CalenderEntries
        WHERE EntryName = ? AND EntryYear = ? AND EntryMonth = ? AND EntryDay = ? AND EntryHour = ? AND EntryMin = ? AND Notes = ? AND LinkedPersons = ? AND AlertTiming = ?"""
        params = (EntryName, entry_date_year, entry_date_month, entry_date_day, entry_date_hour, entry_date_minute, Notes, LinkedPersons, datum_alert_timing_str)
        output_existing_entries = self.db_conn.GetFromDatabase(sql, params)
        if len(output_existing_entries) == 0:


            # Daten des Eintrags in die Datenbank schreiben:
            sql = f"""INSERT INTO CalenderEntries (EntryName, EntryYear, EntryMonth, EntryDay, EntryHour, EntryMin, Notes, LinkedPersons, AlertTiming)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            params = (EntryName, entry_date_year, entry_date_month, entry_date_day, entry_date_hour, entry_date_minute, Notes, LinkedPersons, datum_alert_timing_str)
            self.db_conn.addToDatabase(sql, params)
            return True
        else:
            print('Eintrag ist bereits vorhanden!')
            return False

    def check_for_alert(self):
        # Hole eine Liste des Datums und der Erinnerungszeit aus der Datenbank
        sql = f"SELECT EntryID, EntryYear, EntryMonth, EntryDay, EntryHour, EntryMin, AlertTiming FROM CalenderEntries"
        date_entry_list = self.db_conn.GetFromDatabase(sql, ())

        # schreibe das Datum in eine separate Liste
        date_list = []
        alert_timing_list = []
        entryID_list = []
        for EntryTuple in date_entry_list:
            entryID_list.append(EntryTuple[0])
            entry_datetime = datetime.datetime(EntryTuple[1], EntryTuple[2], EntryTuple[3], EntryTuple[4], EntryTuple[5])
            date_list.append(entry_datetime)
            timedelt_alert_timing = entry_datetime - datetime.datetime.strptime(EntryTuple[6], '%d.%m.%Y %H:%M:%S')
            timedelt_alert_timing = timedelt_alert_timing.total_seconds()
            alert_timing_list.append(timedelt_alert_timing)

        entryID_array = np.array(entryID_list)
        date_array = np.array(date_list)
        alert_timing_array = np.array(alert_timing_list)

        current_datetime = datetime.datetime.now()

        tdelta_cal_entry = date_array - current_datetime
        tdelta_seconds_list = []
        for tdelta_element in tdelta_cal_entry:
            tdelta_seconds_list.append(tdelta_element.total_seconds())
        tdelta_calc_total_seconds = np.array(tdelta_seconds_list)
        # tdelta_calc_total_seconds = tdelta_cal_entry.total_seconds()
        check_tdelta_alert_timing = np.bitwise_and(tdelta_calc_total_seconds >= 0, tdelta_calc_total_seconds <= timedelt_alert_timing)
        pos_active_alerts = np.where(check_tdelta_alert_timing == True)
        pos_active_alerts = pos_active_alerts[0].tolist()
        try:
            active_entryID_array = entryID_array[pos_active_alerts]
            active_tdelta_cal_entry = tdelta_cal_entry[pos_active_alerts]
            # active_cal_entries = np.array(active_entryID_array, active_tdelta_cal_entry)
            return active_entryID_array, active_tdelta_cal_entry
        except:
            return 0
    def do_alert(self, active_entryID_array, active_tdelta_cal_entry):
        if active_entryID_array.size == 0:
            pass
        else:
            i = 0
            for i in range(len(active_entryID_array)):
               # element = active_entryID_array[i]

                EntryID = active_entryID_array[i]
                time_till_event = active_tdelta_cal_entry[i]
                print(f'Das Event mit der ID {EntryID} startet in {time_till_event}')

    def ShowCalender(self, shown_month_year, shown_month_month):
        ## bestimme den letzten Tag des Monats:
        shown_month = shown_month_month
        shown_year = shown_month_year
        shown_next_month = datetime.datetime(shown_year, shown_month+1, 1)
        shown_month_last_day = shown_next_month - datetime.timedelta(days=1)
        days_in_month = shown_month_last_day.day
        #array_days_in_month = np.array(range(1, days_in_month))

        ## Hole alle Einträge, die im Monat bzw. Jahr von shown_month_date angesiedelt sind
        sql = f"""SELECT EntryID, EntryName, EntryYear,
        EntryMonth, EntryDay, EntryHour,
        EntryMin, Notes, LinkedPersons, AlertTiming FROM CalenderEntries WHERE EntryYear = ? AND EntryMonth = ?"""
        params = (shown_year, shown_month)
        entries_in_shown_month = self.db_conn.GetFromDatabase(sql, params)

        entries_in_month = np.empty(days_in_month, dtype=object)
        for i in range(len(entries_in_month)):
            entries_in_month[i] = []
        entry_into_list = []
        for current_entry in entries_in_shown_month:
            pos_day = current_entry[4]
            # entry_into_list.append(current_entry)
            entries_in_month[pos_day].append(current_entry)

        print(entries_in_month)

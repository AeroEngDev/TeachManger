import datetime as dt
import sqlite3
import numpy as np
from DB_con import DB_con
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
import pdb


class Calender:

    def __init__(self, db_connection, calender_frame, parent_window):
        self.parent_window = parent_window
        self.db_connection = db_connection
        self.calender_frame = calender_frame
        self.heading_frame = tk.Frame(self.calender_frame)
        self.heading_frame.grid(column=0, row=0)

        self.cal_number_buttons_frame = tk.Frame(self.calender_frame)
        self.cal_number_buttons_frame.grid(column=0, row=1)

        self.cal_upcoming_events_frame = tk.Frame(self.calender_frame)
        self.cal_upcoming_events_frame.grid(column=0, row=2)

        # upcoming events frame segmentation:
        self.upcoming_events_heading_frame = tk.Frame(self.cal_upcoming_events_frame)
        self.upcoming_events_heading_frame.grid(column=0, row=0)

        self.upcoming_events_content_frame = tk.Frame(self.cal_upcoming_events_frame)
        self.upcoming_events_content_frame.grid(column=0, row=1)

        self.heading_upcoming_event_label = ttk.Label(self.upcoming_events_heading_frame, text='Bevorstehende Termine', style="My.TLabel")
        self.heading_upcoming_event_label.grid(column=0, row=0)
        event_timeing_list = ['1 Tag', '1 Woche', '1 Monat']
        self.selected_upcoming_event_time = tk.StringVar()
        self.selected_upcoming_event_time.set(event_timeing_list[0])
        self.select_upcoming_event_time = tk.OptionMenu(self.upcoming_events_heading_frame, self.selected_upcoming_event_time, *event_timeing_list)
        self.select_upcoming_event_time.grid(column=0, row=1)

        def func(event):
            self.show_next_events()
        self.select_upcoming_event_time.bind('<Configure>', func)
        self.show_next_events()

        # insert the plus button for the creation of a new event:
        photo = tk.PhotoImage(file="plus_button.gif")
        self.plus_button = tk.Button(self.heading_frame, image=photo, command=self.create_new_event)
        self.plus_button.image = photo
        self.plus_button.grid(column=0, row=0)

        self.heading_label = ttk.Label(self.heading_frame, text='Kalender', style="My.TLabel")
        self.heading_label.grid(column=1, row=0)


    def create_new_event(self):
        self.child_window_for_new_cal_entry = tk.Toplevel(self.parent_window)
        self.heading_frame = tk.Frame(self.child_window_for_new_cal_entry)
        self.heading_frame.grid(column=0, row=0)
        self.heading_label_new_cal = ttk.Label(self.heading_frame, text='Neuer Kalendereintrag', style="My.TLabel")
        self.heading_label_new_cal.grid(column=0, row=0)

        self.content_frame = tk.Frame(self.child_window_for_new_cal_entry)
        self.content_frame.grid(column=0, row=1)

        self.label_entry_name = tk.Label(self.content_frame, text='Name des Eintrags')
        self.label_entry_name.grid(column=0, row=0)

        self.entry_widget_name_var = tk.StringVar()
        self.entry_widget_name = tk.Entry(self.content_frame, textvariable=self.entry_widget_name_var, justify=tk.CENTER)
        self.entry_widget_name.grid(column=1, row=0, ipadx=100)

        self.label_date = tk.Label(self.content_frame, text='Zeitpunkt des Events')
        self.label_date.grid(column=0, row=1)

        # set the text of the entry widget the current datetime in 2 hours:
        datetime_now = dt.datetime.now()
        datetime_in_2hours = datetime_now + dt.timedelta(hours=2)

        datetime_round_up_to_full_hours = dt.datetime(datetime_in_2hours.year, datetime_in_2hours.month, datetime_in_2hours.day, datetime_in_2hours.hour)
        self.str_datetime_full_hours = datetime_round_up_to_full_hours.strftime("%d.%m.%Y %H:%M")

        self.entry_date_var = tk.StringVar()
        self.entry_date_var.set(self.str_datetime_full_hours)
        self.entry_date = tk.Entry(self.content_frame, textvariable=self.entry_date_var, justify=tk.CENTER)
        self.entry_date.grid(column=1, row=1, ipadx=100)
        #self.entry_date.bind('<Configure>', self.check_date_entry)

        self.notes_label = tk.Label(self.content_frame, text='Notizen')
        self.notes_label.grid(column=0, row=2)

        self.notes_entry_var = tk.StringVar()
        self.notes_entry = tk.Entry(self.content_frame, textvariable=self.notes_entry_var)
        self.notes_entry.grid(column=1, row=2, ipadx=100, ipady=50)

        self.submit_button_new_cal_entry = tk.Button(self.content_frame, text='Abschicken', command=self.submit_new_cal_entry)
        self.submit_button_new_cal_entry.grid(column=1, row=3)


    def submit_new_cal_entry(self):
        # check if datetime string is interpretable:
        try:
            new_cal_entry_datetime_obj = dt.datetime.strptime(self.entry_date_var.get(), "%d.%m.%Y %H:%M")

        except:
            ok_click = tkinter.messagebox.showerror(title='Fehler!', message='Das Format des Datums war fehlerhaft. Bitte korrigieren!')
            self.entry_date.configure(bg="red")
            self.entry_date_var.set(self.str_datetime_full_hours)
            if ok_click:
                self.child_window_for_new_cal_entry.lift()
                return

        if self.entry_widget_name_var.get() == '':
            ok_click = tkinter.messagebox.showerror(title='Fehler!', message='Der Name darf nicht leer sein!')
            self.entry_widget_name.configure(bg="red")
            if ok_click:
                self.child_window_for_new_cal_entry.lift()
                return

        else:
            sql_insert_new_cal_into_db = "INSERT INTO CalenderEntries (entry_name, date, notes) VALUES (?, ?, ?)"
            params_insert = (self.entry_widget_name_var.get(), new_cal_entry_datetime_obj, self.notes_entry_var.get())
            try:
                self.db_connection.addToDatabase(sql_insert_new_cal_into_db, params_insert)
                on_click = tkinter.messagebox.showinfo(title='Erfolg!', message='Eintrag erfolgreich eingetragen!')
                if on_click:
                    self.child_window_for_new_cal_entry.destroy()
                    return
            except:
                on_click = tkinter.messagebox.showerror(title="Fehler!", message="Event konnte nicht eingetragen werden! Unbekannter Fehler...")
                if on_click:
                    self.child_window_for_new_cal_entry.destroy()
                    return

    def show_next_events(self):
        Shown_events_timing = self.selected_upcoming_event_time.get()
        if Shown_events_timing == '1 Tag':
            event_timing_timedelt = dt.timedelta(days=1)
        elif Shown_events_timing == '1 Woche':
            event_timing_timedelt = dt.timedelta(weeks=1)
        else:
            event_timing_timedelt = dt.timedelta(weeks=4)
        datetime_until_output = dt.datetime.now() + event_timing_timedelt

        sql_get_events_from_db = "SELECT * FROM CalenderEntries WHERE date < ? AND date > ?"
        params_date_selection = (datetime_until_output, dt.datetime.now())
        events_output = self.db_connection.GetFromDatabase(sql_get_events_from_db, params_date_selection)
        self.show_events_treeview = ttk.Treeview(self.upcoming_events_content_frame)
        self.show_events_treeview["columns"] = ('Eintrag ID', 'Eintragsname', 'Zeitpunkt', 'Zeit bis zum Event')
        self.show_events_treeview.column('Eintrag ID')
        self.show_events_treeview.column('Eintragsname')
        self.show_events_treeview.column('Zeitpunkt')
        self.show_events_treeview.column('Zeit bis zum Event')

        self.show_events_treeview.heading('Eintrag ID', text='Eintrag ID')
        self.show_events_treeview.heading('Eintragsname', text='Eintragsname')
        self.show_events_treeview.heading('Zeitpunkt', text='Zeitpunkt')
        self.show_events_treeview.heading('Zeit bis zum Event', text='Zeit bis zum Event')
        for event in events_output:
            self.show_events_treeview.insert('', 'end', values=(event[0], event[1], event[2], 'kommt noch'))

        self.show_events_treeview.grid(column=0, row=0)

    def build_grid(self, year, month):
        date_next_month = dt.datetime(year, month+1, 1)

        date_last_day_of_month = date_next_month - dt.timedelta(days=1)
        self.button_day_list = []
        i = 0
        j = 0

        for day in range(1, date_last_day_of_month.day+1):
            self.button_day_list.append(tk.Button(self.cal_number_buttons_frame, text=day, command=self.calender_day_clicked))
            self.button_day_list[len(self.button_day_list)-1].grid(column=i, row=j)
            i = i + 1
            if i > 5:
                i = 0
                j = j + 1

    def calender_day_clicked(self):
        pass

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

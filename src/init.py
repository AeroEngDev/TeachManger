import os as os
import subprocess
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
import re as re
import datetime as dt
from DB_con import DB_con
import pdb

from work_with_encryption import work_with_crypto


class init:

    def __init__(self, parent_window, content_frame):
        self.create_database_window = None
        self.parent_window = parent_window
        self.content_frame = content_frame
        self.pos_in_msg = 0
        self.msg_check_for_dir = tk.Label(self.content_frame, text='Überprüfe database Ordner...')
        self.msg_check_for_dir.grid(column=0, row=self.pos_in_msg)
        # check if database dir exists:
        output = subprocess.getstatusoutput("ls -la | grep database| grep d")


        if output[0] == 0:
            self.msg_found_dir = tk.Label(self.content_frame, text='database Ordner gefunden...')
            self.pos_in_msg += 1
            self.msg_found_dir.grid(column=0, row=self.pos_in_msg)
            self.check_for_db_files()
        else:
            self.msg_no_dir = tk.Label(self.content_frame, text='Kein database Ordner gefunden, erstelle ihn jetzt.')
            self.pos_in_msg += 1
            self.msg_no_dir.grid(column=0, row=self.pos_in_msg)
            os.system('mkdir database')
            self.check_for_db_files()

    def check_for_db_files(self):
        os.chdir('database/')

        # check if we are in the database dir:
        pwd = subprocess.getstatusoutput('pwd')

        database_reg_exp = re.compile(r'\/database$')
        match_obj = re.match(database_reg_exp, pwd[1])

        if match_obj == 0:
            self.msg_cant_cd_into_dir = tk.Label(self.content_frame, text='Database Ordner konnte nicht betreten werden...')
            self.pos_in_msg += 1
            self.msg_cant_cd_into_dir.grid(column=0, row=self.pos_in_msg)
            return

        self.msg_check_for_db_in_dir = tk.Label(self.content_frame, text='Überprüfe, ob Datenbanken vorhanden sind...')
        self.pos_in_msg += 1
        self.msg_check_for_db_in_dir.grid(column=0, row=self.pos_in_msg)

        databases = self.check_dbs_in_pwd()
        #pdb.set_trace()
        if len(databases) == 1:
            self.msg_found_one_db = tk.Label(self.content_frame, text='Es wurde genau eine Datenbank gefunden. Es wird geprüft, ob sie verschlüsselt ist')
            self.pos_in_msg += 1
            self.msg_found_one_db.grid(column=0, row=self.pos_in_msg)

            self.crypto_obj = work_with_crypto(databases[0], self.content_frame, self.pos_in_msg)
            self.pos_in_msg = self.crypto_obj.get_row_counter()

        elif len(databases) > 1:
            self.msg_found_more_dbs = tk.Label(self.content_frame, text='Es wurden verschiedene Datenbanken gefunden, bitte auswählen...')
            self.pos_in_msg += 1
            self.msg_found_more_dbs.grid(column=0, row=self.pos_in_msg)
            self.db_choice_window = tk.Toplevel(self.parent_window)
            self.db_choice_window.lift()
            self.heading_choice_window_frame = tk.Frame(self.db_choice_window)
            self.content_choice_window_frame = tk.Frame(self.db_choice_window)
            self.heading_choice_window_frame.grid(column=0, row=0)
            self.content_choice_window_frame.grid(column=0, row=1)
            self.heading_label_choice_window = ttk.Label(self.heading_choice_window_frame, text='Datenbank auswählen', style="My.TLabel")
            self.heading_label_choice_window.grid(column=0, row=0)
            self.desc_label_choice_window = tk.Label(self.content_choice_window_frame, text='Es wurden mehr als eine Datenbank gefunden. Bitte wähle die datenbank aus, die du laden möchtest')
            self.desc_label_choice_window.grid(column=0, row=0, columnspan=3)
            self.option_menu_label_choice_db = tk.Label(self.content_choice_window_frame, text='Datenbank wählen:')
            self.option_menu_label_choice_db.grid(column=0, row=1)
            self.option_menu_choice_db_var = tk.StringVar()
            self.option_menu_choice_db = tk.OptionMenu(self.content_choice_window_frame, self.option_menu_choice_db_var, *databases)
            self.option_menu_choice_db.grid(column=1, row=1)

            self.submit_db_choice = tk.Button(self.content_choice_window_frame, text='Abschicken', command=self.submit_choice)
            self.submit_db_choice.grid(column=1, row=2)


        else:
            #pdb.set_trace()
            self.msg_no_db_found = tk.Label(self.content_frame, text='Es konnte keine Datenbank gefunden werden...')
            self.pos_in_msg += 1
            self.msg_no_db_found.grid(column=0, row=self.pos_in_msg)

            self.msg_start_setup_assistent = tk.Label(self.content_frame, text='Setup-Assistent für die Datenbankerstellung wird gestartet...')
            self.pos_in_msg += 1
            self.msg_start_setup_assistent.grid(column=0, row=self.pos_in_msg)
            self.create_new_database()
        #self.db_connection = db_connection
        # build list of database file names:


    def get_row_counter(self):
        return self.pos_in_msg

    def submit_choice(self):
        self.crypto_obj = work_with_crypto(self.option_menu_choice_db_var.get(), self.content_frame, self.pos_in_msg)
        self.pos_in_msg = self.crypto_obj.get_row_counter()
        self.db_choice_window.destroy()

    def return_db_connection(self):
        return self.crypto_obj.get_db_connection()

    def create_new_database(self):
        # setup assistent for new database
        self.create_database_window = tk.Toplevel()
        style = ttk.Style(self.create_database_window)
        #style.configure("TLabel_setup_window", font=('Arial', 25))
        self.setup_heading_frame = tk.Frame(self.create_database_window)
        self.setup_heading_frame.grid(column=0, row=0)
        self.heading_label = tk.Label(self.setup_heading_frame, text='Neue Datenbank erstellen')
        self.heading_label.grid(column=0, row=0)
        self.setup_content_frame = tk.Frame(self.create_database_window)
        self.setup_content_frame.grid(column=0, row=1)

        self.description_label_setup = tk.Label(self.setup_content_frame, text='Da in dieser Datenbank sensibele Daten gespeichert werden können, kann die Datenbank verschlüsselt werden.')
        self.description_label_setup.grid(column=0, row=0)

        self.desc_label_2_setup = tk.Label(self.setup_content_frame, text='Für die Entschlüsselung wird dann ein Passwort benötigt. Bitte beachte, dass bei Verlust des Passworts nicht mehr auf die Datenbank zugegriffen werden kann.')
        self.desc_label_2_setup.grid(column=0, row=1)

        self.desc_label_3_setup = tk.Label(self.setup_content_frame, text='Überlege dir also gut, ob du die Datenbank verschlüsseln möchtest!')
        self.desc_label_3_setup.grid(column=0, row=2)

        self.database_name_label = tk.Label(self.setup_content_frame, text='Datenbank Name')
        self.database_name_label.grid(column=0, row=3)

        self.database_name_entry_var = tk.StringVar()
        # set a default database name containing the current date and time to make the name unique
        self.current_datetime = dt.datetime.now()
        self.current_datetime_str = self.current_datetime.strftime("%d%m%Y_%H%M")
        self.database_name_str = f"Datenbank_{self.current_datetime_str}.db"
        self.database_name_entry_var.set(self.database_name_str)

        self.database_name_entry_widget = tk.Entry(self.setup_content_frame, textvariable=self.database_name_entry_var)
        self.database_name_entry_widget.grid(column=1, row=3)

        self.encrypt_checkbutton_var = tk.IntVar()
        self.encrypt_checkbutton_var.set(0)
        self.encrypt_checkbutton = tk.Checkbutton(self.setup_content_frame, text="Verschlüsseln?", variable=self.encrypt_checkbutton_var, onvalue=1, offvalue=0, command=self.password_widget)
        self.encrypt_checkbutton.grid(column=1, row=4)
        #pdb.set_trace()
        # self.password_label = tk.Label(self.setup_content_frame, text='Verschlüsselungs-Passwort')
        #
        # self.password_entry_var = tk.StringVar()
        # self.password_entry_widget = tk.Entry(self.setup_content_frame, show="*")

        self.submit_button = tk.Button(self.setup_content_frame, text='Abschicken', command=self.submit_new_db)
        self.submit_button.grid(column=1, row=5)



    def password_widget(self):
        if self.encrypt_checkbutton_var.get() == 1:
            self.database_name_entry_var.set(self.database_name_entry_var.get().replace(".db", ".enc"))
        else:
            self.database_name_entry_var.set(self.database_name_entry_var.get().replace(".enc", ".db"))


    def check_dbs_in_pwd(self):
        databases_str = subprocess.getstatusoutput('ls | grep .db')

        # reg_exp_new_line = re.compile(r'[\S]+(.db)|[\S]+(.enc)')
        # pdb.set_trace()
        # return re.findall(reg_exp_new_line, databases_str[1])
        return databases_str[1].splitlines()

    def submit_new_db(self):
        # check if database name already exists:
        db_results = self.check_dbs_in_pwd()
        new_db_name = self.database_name_entry_var.get()
        for db_name in db_results:
            if new_db_name == db_name:
                on_click = tkinter.messagebox.showerror(title='Name schon vorhanden!', message='Datenbank Name schon vorhanden. Bitte anderen Namen wählen!')
                if on_click:
                    self.database_name_entry_widget.configure(bg="red")
                    self.create_database_window.lift()
                    return

        #check if a password was given:
        if self.encrypt_checkbutton_var == 1:
            if len(self.password_entry_var.get()) < 10:
                on_click = tkinter.messagebox.showerror(title='Passwort zu kurz', message="Das Passwort muss mindestens 10 zeichen lang sein!")
                if on_click:
                    self.password_entry_widget.configure(bg='red')
                    self.create_database_window.lift()
                    return
            else:
                self.crypto_obj = work_with_crypto(new_db_name, self.content_frame, self.pos_in_msg)
                self.pos_in_msg = self.crypto_obj.get_row_counter()
        else:
            self.crypto_obj = work_with_crypto(new_db_name, self.content_frame, self.pos_in_msg)
            self.pos_in_msg = self.crypto_obj.get_row_counter()
            self.create_database_window.destroy()

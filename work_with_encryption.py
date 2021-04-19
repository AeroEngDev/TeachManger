from Crypto.Cipher import AES
import os
import binascii
from backports.pbkdf2 import pbkdf2_hmac
import pdb
from DB_con import DB_con
import tkinter as tk
import tkinter.ttk as ttk


class work_with_crypto:

    def __init__(self, current_file_name, content_frame, row_counter):
        self.content_frame = content_frame
        self.row_counter = row_counter
        str_dot_pos = current_file_name.find(".")
        if current_file_name[str_dot_pos+1:len(current_file_name)] == "enc":
            # file is encrypted: Start decryption algorithm
            self.msg_db_enc = tk.Label(self.content_frame, text='Die Datenbank ist verschlüsselt!')
            self.row_counter += 1
            self.msg_db_enc.grid(column=0, row=self.row_counter)

            # build a window for the password input
            self.password_entry_window = tk.Toplevel(self.parent_window)
            self.heading_pw_window_frame = tk.Frame(self.password_entry_window)
            self.content_pw_window_frame = tk.Frame(self.password_entry_window)
            self.heading_pw_window_frame.grid(column=0, row=0)
            self.content_pw_window_frame.grid(column=0, row=1)

            self.heading_pw_window_label = ttk.Label(self.heading_pw_window_frame, text='Passwort benötigt:', style="My.TLabel")
            self.heading_pw_window_label.grid(column=0, row=0)

            self.pw_entry_label_dec = tk.Label(self.content_pw_window_frame, text='Passwort')
            self.pw_entry_label_dec.grid(column=0, row=0)

            self.pw_entry_widget_dex_var = tk.StringVar()
            self.pw_entry_widget_dex = tk.Entry(self.content_pw_window_frame, textvariable=self.pw_entry_widget_dex_var, show='*')
            self.pw_entry_widget_dex.grid(column=1, row=0)

            self.submit_button_pw_window = tk.Button(self.content_pw_window_frame, text='Abschicken', command=self.submit_password)

        elif current_file_name[str_dot_pos+1:len(current_file_name)] == "db":
            # the file is not encrypted: Just open it!
            self.msg_db_not_enc = tk.Label(self.content_frame, text='Die Datenbank ist nicht verschlüsselt, und wird nun geöffnet!')
            self.row_counter += 1
            self.msg_db_not_enc.grid(column=0, row=self.row_counter)
            self.db_connection = DB_con(current_file_name)

        else:
            self.msg_error_open_db = tk.Label(self.content_frame, text='Dateiname war fehlerhaft! Bitte checke die Dateierweiterung. Es können nur Dateinamen mit .enc und .db eingelesen werden!')
            self.row_counter += 1
            self.msg_error_open_db.grid(column=0, row=self.row_counter)

    def get_row_counter(self):
        return self.row_counter

    def get_db_connection(self):
        return self.db_connection

    def submit_password(self):
        self.key_creation(self.pw_entry_widget_dex_var.get())

    def key_creation(self, password):
        self.db_name = db_name
        # let DB_Con try to connect to the database
        # if it fails, it is likely that the file is encrypted
        # salt = binascii.unhexlify(os.urandom(128))
        salt = b'\xacwS\xd5\xa9\x95\x80\x10\x0cJ\x99\r\x0f\x90\xa5\xf7,\xe8f\xb8\x8a\x8b\xees\x98\x1e\x82}d\x05c\xa8_\x91\xa9(q\xf8?\x87"!\xc7\x87\x8d\\\x95&\xc1F6\x0b\xf2&\xcb-\x1ct\x7f\xdf\\\x86\x91w\x9a~Y\xacg\xa0\xc7\xda\x05\x81\xa3\x81\xfa\xee\xd3h\xa3f\x93V$ \x92\xa6\x8c\x8b68iu`\x15\x00\xcf\x0e`\xaaA\xc9q\xc3\xedCN\xeb\xc4/\xb33]G\x11\x81\xb2\xf6\x98b\x0f\xb5\x0b\xca\xe5\xdb\xf5'
        key = pbkdf2_hmac("sha256", str.encode(password), salt, 100000, 16)
        pdb.set_trace()
        self.cipher = AES.new(key, AES.MODE_EAX)

        print(key)

    def pad(self, s):
        return s + b'\0'*(AES.block_size - len(s))

    def encrypt(self, message):
        message = self.pad(message)
        return self.cipher.encrypt(message)

    def encrypt_file(self):
        with open(self.file_name) as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext)
        self.file_name_enc = self.file_name.replace(".db", ".enc")
        with open(self.file_name_enc, "w") as fi:
            fi.write(enc)
        os.remove(self.file_name)

    def decrypt(self, message):
        message = self.pad(message)
        return self.cipher.decrypt(message)

    def decrypt_file(self):
        with open(self.file_name) as fo:
            cipher_text = fo.read()
        db = self.decrypt(cipher_text)
        self.file_name_db = self.file_name.replace(".enc", ".db")
        with open(self.file_name_db, "w") as fi:
            fi.write(db)
        os.remove(self.file_name)
        self.db_connection = DB_con(self.file_name_db)

    # def open_db(self):
    #     os.chdir('database/')
    #     self.encrypted_file = "encrypted.db"
    #     with open(self.db_name, "rb") as ifile:
    #         with open(self.encrypted_file, "w") as ofile:
    #             data_chunk = ifile.read(16)
    #             if len(data_chunk) < 16:
    #                 while len(data_chunk) % 16 == 0:
    #                     data_chunk.append(' ')
    #             ciphertext = self.cipher.encrypt_and_digest(data_chunk)
    #             ofile.write(ciphertext)
    #             while data_chunk:
    #                 data_chunk = ifile.read(16)
    #                 if len(data_chunk) < 16:
    #                     while len(data_chunk) % 16 == 0:
    #                         data_chunk.append(' ')
        #pdb.set_trace()

    # def take_16bit_chunks(self, data, pos_handler):
    #     pass
    #     #data[]

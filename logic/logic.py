import os
import requests
import re as regEx
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication
from logic.constants import *

class ApplicationLogic(QObject):
    # SIGNALS
    DISPLAY_TERMINAL_SIGNAL = Signal(str, str)
    DISPLAY_DB_ID_SIGNAL = Signal(str)
    DISPLAY_CREDENTIALS_SIGNAL = Signal(object)

    def save_credentials(self, prn, seat_num, db_id):
        data = DB_INSTANCE.database_action('add', prn, seat_num, db_id)
        self.get_credentials()
        return data

    def get_credentials(self, prn=0, seat_num=0, db_id=0):
        data = DB_INSTANCE.database_action('get', prn, seat_num, db_id)
        self.emit_credentials(data)
        return data

    def download(self, prn, response):
        base_path = os.path.dirname(os.path.abspath(__file__)) + r'\results'
        if os.path.exists(base_path) == False:
            os.makedirs(base_path)

        output_path = os.path.join(base_path, f"result_{str(prn)}.pdf")
        with open(output_path, 'wb') as file:
            file.write(response.content)
            file.close()

        if(os.path.exists(output_path)):
            os.startfile(base_path)
            return True
        else:
            self.download(prn, response)

    def process_download_url(self, download_url, prn, quick):
        while (self.download_opn):
            response = requests.get(download_url)
            if (response.status_code == 200):
                if (self.download(prn, response)):
                    self.db = True
                    self.download_opn = False
                    return True 
            elif response.status_code == 404:
                self.emit_signal('not found', 'terminating...')
                if not (quick):
                    self.operation = False
                else:
                    return False
            elif response.status_code == 503:
                self.emit_signal('server down', 'retrying...') 
            else:
                self.emit_signal.emit('unexpected error', f'code - {response.status_code}')

    def generate_download_url(self, db_id):
        download_url = f'{DOWNLOAD_URL_P1}{db_id}{DOWNLOAD_URL_P2}'
        return download_url

    def validate_response(self, msg):
        if(msg in E_ARRAY_MSG):
            if msg == E_ARRAY_MSG[2]:
                self.emit_signal('error', E_ARRAY_MSG[2])
                return False
            self.emit_signal('error', msg)
            return False
        else:
            return True

    def generate_final_url(self, seat_num, db_id):
        final_url = f'{FINAL_URL_P1}{db_id}{FINAL_URL_P2}{seat_num}'
        return final_url

    def process_final_url(self, final_url, db_id, quick):
        while (self.final):
            response = requests.get(final_url)
            if (response.status_code == 200):
                msg = response.text
                if (self.validate_response(msg)):
                    download_url = self.generate_download_url(db_id)
                    self.final = False
                    return download_url
                else:
                    self.download_opn = False
                    self.final = False
                    self.operation = False
            elif response.status_code == 404:
                self.emit_signal('not found', 'terminating...')
                if not (quick):
                    self.operation = False
            elif response.status_code == 503:
                self.emit_signal('server down', 'retrying...') 
            else:
                self.emit_signal.emit('unexpected error', f'code - {response.status_code}')

    def get_database_id(self, response):
        pattern = PATTERN
        match = regEx.search(pattern, response)
        db_id = match.group(1)
        self.emit_db_id(db_id)
        return db_id

    def generate_initial_url(self, prn):
        initial_url = f'{INITIAL_URL_P1}{prn}{INITIAL_URL_P2}'
        return initial_url

    def emit_credentials(self, data):
        self.DISPLAY_CREDENTIALS_SIGNAL.emit(data)
        return True

    def emit_db_id(self, db_id):
        self.DISPLAY_DB_ID_SIGNAL.emit(db_id)
        return True

    def emit_signal(self, message_type, message):
        self.DISPLAY_TERMINAL_SIGNAL.emit(message_type, message)
        return True

    def run(self, prn, seat_num, db_id, quick):
        self.operation = True
        self.initial = True
        self.final = True
        self.download_opn = True
        self.db = False

        if not (quick):
            initial_url = self.generate_initial_url(prn)
            while (self.operation):
                QApplication.sendPostedEvents()
                while (self.initial):
                    response = requests.get(initial_url)
                    if (response.status_code == 200):
                        response = response.text
                        if (self.validate_response(response)):
                            db_id = self.get_database_id(response)
                            final_url = self.generate_final_url(seat_num, db_id)
                            self.initial = False
                        else:
                            self.operation = False
                    elif response.status_code == 404:
                        self.emit_signal('not found', 'terminating...')
                        self.final = False
                        self.download_opn = False
                        self.operation = False
                    elif response.status_code == 503:
                        self.emit_signal('server down', 'retrying...') 
                    else:
                        self.emit_signal.emit('unexpected error', f'code - {response.status_code}')                                         

                download_url = self.process_final_url(final_url, db_id, quick)
                self.process_download_url(download_url, prn, quick)

                if (self.db):
                    self.save_credentials(prn,seat_num, db_id)
                    self.emit_signal.emit('Complete:', f'file generated.')
                    self.operation = False
        else:
            download_url = self.generate_download_url(db_id)
            while (self.download_opn):
                QApplication.sendPostedEvents()
                if not(self.process_download_url(download_url, prn, quick)):
                    download_url = self.process_final_url(final_url, db_id)
                    self.process_download_url(download_url, prn, quick)
            self.emit_signal.emit('Complete:', f'file generated.')

import os
import requests
import re as regEx
from time import sleep
from PySide6.QtCore import QObject, Signal
from logic.emitter import SignalEmitter
from logic.constants import *

class ApplicationLogic(QObject):
    # SIGNALS
    DISABLE_RUN_SIGNAL = Signal()
    DISPLAY_TERMINAL_SIGNAL = Signal(str, str)
    DISPLAY_DB_ID_SIGNAL = Signal(str)
    DISPLAY_CREDENTIALS_SIGNAL = Signal(object)

    def __init__(self):
        super(ApplicationLogic, self).__init__()
        self.emitter = SignalEmitter()
        self.emitter.THREAD_SIGNAL.connect(self.emit_signal)
        self.emitter.start()

    def save_credentials(self, prn, seat_num, db_id):
        data = DB_INSTANCE.database_action('add', prn, seat_num, db_id)
        self.get_credentials()
        return data

    def get_credentials(self, prn=0, seat_num=0, db_id=0):
        data = DB_INSTANCE.database_action('get', prn, seat_num, db_id)
        self.emit_credentials(data)
        return data

    def download(self, prn, response):
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        results_dir = os.path.join(parent_dir, 'results')
        os.makedirs(results_dir, exist_ok=True)
        output_path = os.path.join(results_dir, f"result_{str(prn)}.pdf")

        with open(output_path, 'wb') as file:
            file.write(response.content)
            file.close()

        if(os.path.exists(output_path)):
            os.startfile(results_dir)
            return True
        else:
            self.download(prn, response)

    def process_download_url(self, download_url, prn, quick):
        while (self.download_opn):
            try:
                response = requests.get(download_url)
                if (response.status_code == 200):
                    if (self.download(prn, response)):
                        self.db = True
                        self.download_opn = False
                        return True 
                elif response.status_code == 404:
                    self.emitter.add_message('not found', 'terminating...')
                    if not (quick):
                        self.operation = False
                    else:
                        return False
                elif response.status_code == 503:
                    self.emitter.add_message('server down', 'retrying...') 
                else:
                    self.emitter.add_message('unexpected error', f'code - {response.status_code}')
            except (
                    requests.exceptions.ChunkedEncodingError
                    or requests.exceptions.ConnectionError
                    or ConnectionResetError
                ):
                self.emitter.add_message('timeout required', f'restarting in 10 seconds...')
                sleep(10)

    def generate_download_url(self, db_id):
        download_url = f'{DOWNLOAD_URL_P1}{db_id}{DOWNLOAD_URL_P2}'
        return download_url

    def validate_response(self, msg):
        if(msg in E_ARRAY_MSG):
            self.emitter.add_message('error', msg)
            return False
        else:
            return True

    def generate_final_url(self, seat_num, db_id):
        final_url = f'{FINAL_URL_P1}{db_id}{FINAL_URL_P2}{seat_num}'
        return final_url

    def process_final_url(self, final_url, db_id, quick):
        while (self.final):
            try:
                response = requests.get(final_url)
                if (response.status_code == 200):
                    msg = response.text
                    if (self.validate_response(msg)):
                        download_url = self.generate_download_url(db_id)
                        self.final = False
                        return download_url
                    else:
                        self.end()
                elif (response.status_code == 404):
                    self.emitter.add_message('not found', 'terminating...')
                    if not (quick):
                        self.end()
                elif (response.status_code == 503):
                    self.emitter.add_message('server down', 'retrying...')
                else:
                    self.emitter.add_message('unexpected error', f'code - {response.status_code}')
            except (requests.exceptions.ConnectionError or requests.exceptions.HTTPError):
                self.emitter.add_message('ConnectionError:', 'Please check your internet connection...\nRetrying in 7 seconds...')
                sleep(7)
            except (requests.exceptions.RequestException) as e:
                self.emitter.add_message('unexpected error', f'{e}')

    def process_initial_url(self, initial_url, seat_num):
        while (self.initial):
            try:
                response = requests.get(initial_url)
                if (response.status_code == 200):
                    response = response.text
                    if (self.validate_response(response)):
                        db_id = self.get_database_id(response)
                        final_url = self.generate_final_url(seat_num, db_id)
                        self.initial = False
                        return db_id, final_url
                    else:
                        self.end()
                elif (response.status_code == 404):
                    self.emitter.add_message('not found', 'terminating...')
                    sleep(2)
                    self.end()
                elif (response.status_code == 503):
                    self.emitter.add_message('server down', 'retrying...')
                else:
                    self.emitter.add_message('unexpected error', f'code - {response.status_code}')
            except (requests.exceptions.ConnectionError or requests.exceptions.HTTPError):
                self.emitter.add_message('ConnectionError', 'Please check your internet connection...\nRetrying in 7 seconds...')
                sleep(7)
            except (requests.exceptions.RequestException) as e:
                self.emitter.add_message('unexpected error', f'{e}')

    def get_database_id(self, response):
        match = regEx.search(PATTERN, response)
        try:
            db_id = match.group(1)
            self.emit_db_id(db_id)
            return db_id
        except AttributeError:
            self.emitter.add_message('unexpected error', 'please check your credentials')
            sleep(2)
            self.end()
            return False

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

    def emit_run_state_toggle(self):
        self.DISABLE_RUN_SIGNAL.emit()
        return True

    def end(self):
        self.operation = False
        self.initial = False
        self.final = False
        self.emit_run_state_toggle()
        self.download_opn = False

    def run(self, prn, seat_num, db_id, quick):
        self.emit_run_state_toggle()
        self.operation = True
        self.initial = True
        self.final = True
        self.download_opn = True
        self.db = False

        if not (quick):
            initial_url = self.generate_initial_url(prn)
            while (self.operation):
                try:
                    db_id, final_url = self.process_initial_url(initial_url, seat_num)
                except TypeError:
                    pass
                if (db_id and final_url):
                    download_url = self.process_final_url(final_url, db_id, quick)
                    self.process_download_url(download_url, prn, quick)

                if (self.db):
                    self.save_credentials(prn,seat_num, db_id)
                    self.emitter.add_message('Complete', f'file generated.')
                    self.operation = False
        else:
            download_url = self.generate_download_url(db_id)
            while (self.download_opn):
                if not(self.process_download_url(download_url, prn, quick)):
                    download_url = self.process_final_url(final_url, db_id)
                    self.process_download_url(download_url, prn, quick)
            self.emitter.add_message('Complete', f'file generated.')
            self.end()

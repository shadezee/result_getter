import threading
from PySide6.QtCore import Qt, QEvent, Slot
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QIcon, QKeyEvent
import ui.res
from ui.UI_SIU_WEB import *
from logic.logic import ApplicationLogic
from logic.emitter import SignalEmitter

class Widget(QWidget, Ui_siu_web):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(':/icon.ico'))

        self.btn_run.clicked.connect(self.run)
        self.ln_uid.setEnabled(False)
        self.ln_seat_no.setEnabled(True)

        self.logic = ApplicationLogic()
        self.emitter = SignalEmitter()

        self.logic.DISABLE_RUN_SIGNAL.connect(self.toggle_run_state)
        self.logic.DISPLAY_TERMINAL_SIGNAL.connect(self.display_message)
        self.logic.DISPLAY_DB_ID_SIGNAL.connect(self.display_db_id)
        self.logic.DISPLAY_CREDENTIALS_SIGNAL.connect(self.refresh_credential_list)
        self.emitter.THREAD_SIGNAL.connect(self.display_message)
        self.lst_credentials.itemSelectionChanged.connect(self.auto_fill)

        self.generate_credential_list()
        self.lst_credentials.setCurrentRow(0)
        self.ln_prn.installEventFilter(self)
        self.ln_seat_no.installEventFilter(self)
        self.lst_credentials.installEventFilter(self)
        self.btn_run.installEventFilter(self)

    @Slot()
    def auto_fill(self):
        try:
            selected_items = self.lst_credentials.selectedItems()
            selected_item = selected_items[0]
            item_text = selected_item.text()

            if not (item_text == "-----------------------------------------------------"):
                parts = item_text.split(", ")
                prn = parts[1].split(": ")[1]
                seat_num = parts[2].split(": ")[1]
                db_id = parts[3].split(": ")[1]

                self.ln_prn.setText(prn)
                self.ln_seat_no.setText(seat_num)
                self.ln_uid.setText(db_id)
            else:
                self.ln_prn.clear()
                self.ln_seat_no.clear()
                self.ln_uid.clear()
                self.ln_uid.setPlaceholderText('Database ID')
        except IndexError:
            return False
        return True

    @Slot(object)
    def refresh_credential_list(self, data):
        self.lst_credentials.clear()
        self.lst_credentials.addItem("-----------------------------------------------------")
        for id, prn, seat_num, db_id in data:
            self.lst_credentials.addItem(f"ID: {id}, PRN: {prn}, Seat No: {seat_num}, DB: {db_id}")
        return True

    @Slot(str)
    def display_db_id(self, db_id):
        self.ln_uid.setPlaceholderText(db_id)
        return True

    @Slot(str, str)
    def display_message(self, message_type, message):
        self.te_display_terminal.setText(f'{message_type}: {message}')
        return True

    @Slot()
    def toggle_run_state(self):
        btn_state = self.btn_run.isEnabled()
        self.setEnabled(not btn_state)
        return True

    def validate_selection_and_input(self, selected_item, prn, seat_num):
        item_text = selected_item.text()

        parts = item_text.split(", ")
        _prn = parts[1].split(": ")[1]
        _seat_num = parts[2].split(": ")[1]

        if ((_prn == str(prn)) and (_seat_num == str(seat_num))):
            return True
        else:
            self.ln_uid.clear()
            self.ln_uid.setPlaceholderText('Database ID')
            return False

    def generate_credential_list(self):
        self.logic.get_credentials()
        return True

    def get_db_id(self):
        db_id = self.ln_uid.text()
        if not (db_id):
            return 0
        else: 
            return db_id

    def get_seat_num(self):
        try:
            seat_num = int(self.ln_seat_no.text())
            return seat_num
        except ValueError:
            self.te_display_terminal.setText('Please enter a valid seat number.')
            return False

    def get_prn(self):
        try:
            prn = int(self.ln_prn.text())
            return prn
        except ValueError:
            self.te_display_terminal.setText('Please enter a valid PRN.')
            return False

    def eventFilter(self, obj, event):
        if (event.type() == QEvent.KeyPress) and (event.key() == (Qt.Key_Return  or Qt.Key_Enter)):
            self.run()
            return True
        return False

    def run(self):
        prn = self.get_prn()
        seat_num = self.get_seat_num()
        db_id = self.get_db_id()

        if (prn and seat_num):
            self.te_display_terminal.clear()
            selected_items = self.lst_credentials.selectedItems()
            selected_item = selected_items[0]

            if (self.lst_credentials.row(selected_item) == 0):
                quick = False
            elif (self.validate_selection_and_input(selected_item, prn, seat_num)):
                quick = True
            else:
                quick = False
                db_id = 0

            self.display_message('Running', f'for {prn}.')
            threading.Thread(target=self.logic.run, args=(prn, seat_num, db_id, quick)).start()

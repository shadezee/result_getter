from PySide6.QtCore import Signal, QThread, QMutex

class SignalEmitter(QThread):
    signal = Signal(str, str)

    def __init__(self, parent=None):
        super(SignalEmitter, self).__init__(parent)
        self.message_queue = []
        self.mutex = QMutex()
        self.running = True

    def run(self):
        while self.running:
            self.mutex.lock()
            if self.message_queue:
                message_type, message = self.message_queue.pop(0)
                self.signal.emit(message_type, message)
            self.mutex.unlock()
            self.msleep(200)
        return True

    def add_message(self, message_type, message):
        self.mutex.lock()
        self.message_queue.append((message_type, message))
        self.mutex.unlock()
        self.msleep(100)
        return True

    def stop(self):
        self.running = False
        return True

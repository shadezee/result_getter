import sys
from PySide6 import QtWidgets
from ui.widget import Widget
from ui.UI_SIU_WEB import *

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = Widget()
    widget.show()
    app.exec()

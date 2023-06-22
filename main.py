import sys
from PyQt5 import QtWidgets, QtGui
from start_dialog import StartDialog

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    start_dialog = StartDialog()
    if start_dialog.exec_() == QtWidgets.QDialog.Accepted:
        sys.exit(app.exec_())

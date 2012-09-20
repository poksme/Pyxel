from PyQt4 import QtGui

class Box(QtGui.QMessageBox):

    def __init__(self, text, parent = None):
        super(Box, self).__init__(parent)
        self.initUI(text)

    def initUI(self, text):
        self.setText(text)
        self.exec_()

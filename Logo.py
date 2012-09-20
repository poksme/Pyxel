from PyQt4 import QtGui, QtCore

class Logo(QtGui.QWidget, QtCore.QObject):

    def __init__(self, parent = None):
        super(Logo, self).__init__(parent)
        self.initUI(parent)

    def initUI(self, parent):
        self.parent = parent
        self.label = QtGui.QLabel(self)
        self.image = QtGui.QPixmap('pix/logo.png')
        self.label.setPixmap(self.image)
        self.label.setGeometry(0, 0, 160 * self.parent.parent.cte, 30 * self.parent.parent.cte)
        self.label.animate = QtCore.QPropertyAnimation(self, "geometry")
        self.label.animate.setDuration(1770)
        self.label.animate.setStartValue(QtCore.QRect(0, -60 , 160, 144))
        self.label.animate.setEndValue(QtCore.QRect(0, 55, 160, 144))
        self.label.animate.start()

width = 300
height = 400

from PyQt4 import QtGui
import gb

class Screen(QtGui.QWidget):
    def __init__(self, parent = None):
        super(Screen, self).__init__(parent)
        self.initUI(parent)

    def initUI(self, parent):
        self.parent = parent
        self.image = QtGui.QImage(width * self.parent.cte, height * self.parent.cte, \
                                      QtGui.QImage.Format_RGB32)
        self.image.fill(gb.color[self.parent.pal][0])

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.drawImage(0, 0, self.image)
        qp.end()

    def recolor(self):
        self.image.fill(gb.color[self.parent.pal][0])

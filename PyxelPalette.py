try:
    from PyQt4 import QtGui, QtCore
except ImportError:
    from PySide import QtGui, QtCore
import gb, pos

class PyxelPalette(QtGui.QWidget):

    def __init__(self, parent = None):
        super(PyxelPalette, self).__init__(parent)
        self.initUI(parent)

    def initUI(self, parent):
        self.parent = parent

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        qp.end()

    def drawRectangles(self, qp):
        h = pos.paletteH * self.parent.cte / 4
        qp.setPen(QtGui.QColor(0))
        for i in xrange(4):
            if (i != self.parent.colsel):
                qp.setBrush(QtGui.QColor(gb.color[self.parent.pal][i]))
                qp.drawRect(0, i * h , h , h)

        qp.setPen(QtGui.QColor(255, 255, 255))
        qp.setBrush(QtGui.QColor(gb.color[self.parent.pal][self.parent.colsel]))
        qp.drawRect(0, self.parent.colsel * h , h , h)


    def mousePressEvent(self, e):
        self.parent.colsel = e.pos().y() / (pos.paletteH * self.parent.cte / 4)
        self.repaint()
        self.parent.brushWidget.repaint()

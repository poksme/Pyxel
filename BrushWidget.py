try:
    from PyQt4 import QtGui, QtCore
except ImportError:
    from PySide import QtGui, QtCore
import gb, pos, math

class BrushWidget(QtGui.QWidget):

    def __init__(self, parent = None):
        super(BrushWidget, self).__init__(parent)
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
        qp.setBrush(QtGui.QColor(gb.color[self.parent.pal][self.parent.colsel]))
        for i in xrange(4):
            if (i != self.parent.brush):
                size = max(h / 3 * i, 4)
                qp.drawRect(0 + (h / 2) - size / 2, i * h + (h / 2) - size / 2, size, size)

        qp.setPen(QtGui.QColor(255, 255, 255))
        size = max(h / 3 * self.parent.brush, 4)
        qp.drawRect(0 + (h / 2) - size / 2, self.parent.brush * h + (h / 2) - size / 2, size, size)


    def mousePressEvent(self, e):
        self.parent.brush = e.pos().y() / (pos.paletteH * self.parent.cte / 4)
        self.repaint()

#PyxelBoard

import sys, math
from PyQt4 import QtGui, QtCore
import win, gb, PyxelBoard, pos, Error, Logo

class PyxelBoard(QtGui.QWidget):

    def __init__(self, parent = None):
        super(PyxelBoard, self).__init__(parent)
        self.initUI(parent)

    def initUI(self, parent):
        self.parent = parent
        self.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.image = QtGui.QImage(gb.width * self.parent.cte, gb.height * self.parent.cte, \
                                      QtGui.QImage.Format_RGB32)
        self.clearBoard()
        # self.image.fill(gb.color[self.parent.pal][0])
        self.logo = Logo.Logo(self)
        self.oldx = -1
        self.oldy = -1

    def clearBoard(self):
        self.image.fill(gb.color[self.parent.pal][0])
        self.repaint()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.drawImage(0, 0, self.image)
        qp.end()

    def customPxl(self, x, y):
        if (x >= 0 and y >= 0 and x < gb.width * self.parent.cte and y < gb.height * self.parent.cte):
            self.image.setPixel(x, y, gb.color[self.parent.pal][self.parent.colsel])

    def recCte(self, x, y, cte):
        if (cte > 1):
            qp = QtGui.QPainter()
            x -= cte / 2
            y -= cte / 2
            x = x - (x % self.parent.cte)
            y = y - (y % self.parent.cte)
            if x != self.oldx or y != self.oldy:
                qp.begin(self.image)
                # qp.setPen(QtGui.QColor(gb.color[self.parent.pal][self.parent.colsel]))
                # qp.setBrush(
                qp.fillRect(x, y, cte, cte, QtGui.QColor(gb.color[self.parent.pal][self.parent.colsel]))
                qp.end()
                self.oldx = x
                self.oldy = y
        else:
            self.customPxl(x, y)

    def drawPxl(self, x, y):
        self.recCte(x, y, self.parent.cte * int(((self.parent.brush + 1) * 1.75)) )

    def drawLine(self, x0, y0, x1, y1):
        steep = (abs(y1 - y0) > abs(x1 - x0))
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        deltax = x1 - x0
        deltay = abs(y1 - y0)
        error = deltax / 2
        y = y0
        if y0 < y1:
            ystep = 1 
        else: 
            ystep = -1
        for x in range(x0, x1):
            if steep:
                self.drawPxl(y,x) 
            else:
                self.drawPxl(x,y)
            error = error - deltay
            if error < 0:
                y = y + ystep
                error = error + deltax

    def mouseMoveEvent(self, e):
        self.x1 = e.pos().x() - (e.pos().x() % self.parent.cte) + self.parent.cte
        self.y1 = e.pos().y() - (e.pos().y() % self.parent.cte) + self.parent.cte
        self.drawLine(self.x0, self.y0, self.x1, self.y1)
        self.x0 = self.x1
        self.y0 = self.y1
        self.repaint()

    def mousePressEvent(self, e):
        if (self.parent.logoFlag == True):
            self.logo.hide()
            self.parent.logoFlag = False
        self.x0 = e.pos().x() - (e.pos().x() % self.parent.cte) + self.parent.cte
        self.y0 = e.pos().y() - (e.pos().y() % self.parent.cte) + self.parent.cte
        self.drawPxl(self.x0, self.y0)
        self.repaint()

    def saveAs(self):
        if (self.parent.cte > 1):
            self.image = self.image.scaled(gb.width, gb.height)
        name, f = QtGui.QFileDialog.getSaveFileNameAndFilter(self, 'Save file', '.', \
                            "Any File (enter your own image type) *;;Bitmap *.bmp;;JPEG *.jpg;;PNG *.png")
        try:
            f = f.split("*")[1]
        except IndexError:
            return
        if (self.image.save(name + f) == False):
            Error.Box("You need to specify an image type", self)
            if (self.parent.cte > 1):
                self.image = self.image.scaled(gb.width * self.parent.cte, gb.height * self.parent.cte)
            self.saveAs()
        if (self.parent.cte > 1):
            self.image = self.image.scaled(gb.width * self.parent.cte, gb.height * self.parent.cte)

    def recolor(self, flag):
        if flag:
            old = self.parent.pal - 1
        else:
            old = (self.parent.pal + 1) % 12
        if (self.parent.cte > 1):
            self.image = self.image.scaled(gb.width, gb.height)
        for i in xrange(gb.width):
            for j in xrange(gb.height):
                for k in xrange(4):
                    if QtGui.QColor.fromRgb(self.image.pixel(i, j)) == QtGui.QColor.fromRgb(gb.color[old][k]):
                        self.image.setPixel(i, j, gb.color[self.parent.pal][k])
        if (self.parent.cte > 1):
            self.image = self.image.scaled(gb.width * self.parent.cte, gb.height * self.parent.cte)

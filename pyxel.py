#!/usr/bin/python
# -*- coding: utf-8 -*-

#pyxel

"""
Pyxel

IT student pixel art project in python using Qt

author: Bertrand "Poksme" Boustany
website: poksme.com
last edited: April 2012
"""

import sys, math
sys.dont_write_bytecode = True
from PyQt4 import QtGui, QtCore, QtSvg
import win, gb, PyxelBoard, PyxelPalette, pos, BrushWidget, Logo, Screen

class MainWidget(QtGui.QWidget):

    def __init__(self, parent = None):
        super(MainWidget, self).__init__(parent)
        self.initUI()
        self.parent = parent

    def initUI(self):
        self.cte = min(win.width / (gb.width + 200), \
                           win.height / (gb.height + 100))
        self.colsel = 2
        self.brush = 0
        self.pal = 0
        self.logoFlag = True

        self.screen = Screen.Screen(self)
        self.screen.setGeometry(0, 0, Screen.width * self.cte, Screen.height * self.cte)

        self.background = QtSvg.QSvgWidget("pix/bg2.svg", self)
        self.background.setGeometry(0, 0, pos.backgroundW * self.cte, \
                                        pos.backgroundH * self.cte)
        self.board = PyxelBoard.PyxelBoard(self)
        self.board.setGeometry(pos.boardX * self.cte, pos.boardY * self.cte, \
                                   gb.width * self.cte, gb.height * self.cte)
        self.palette = PyxelPalette.PyxelPalette(self)
        self.palette.setGeometry(pos.paletteX * self.cte, pos.paletteY * self.cte, \
                                     pos.paletteW * self.cte, pos.paletteH * self.cte + 1)
        self.brushWidget = BrushWidget.BrushWidget(self)
        self.brushWidget.setGeometry((pos.paletteX + pos.space) * self.cte, pos.paletteY * self.cte, \
                                         pos.paletteW * self.cte, pos.paletteH * self.cte + 1)

    def resizeEvent(self, e):
        size = e.size()
        new_cte = min(size.width() / (gb.width + 200), \
                           size.height() / (gb.height + 100))
        if new_cte != self.cte \
                and new_cte:
            self.cte = new_cte
            if (self.logoFlag):
                self.logoFlag = False
                self.board.logo.hide()

            self.board.image = self.board.image.scaled(gb.width * self.cte, \
                                                           gb.height * self.cte)

            self.board.setGeometry(pos.boardX * self.cte, pos.boardY * self.cte, \
                                       gb.width * self.cte, gb.height * self.cte)
            self.board.repaint()
            self.board.logo.repaint()
            self.background.setGeometry(0, 0, pos.backgroundW * self.cte, \
                                            pos.backgroundH * self.cte)
            self.palette.setGeometry(pos.paletteX * self.cte, pos.paletteY * self.cte, \
                                         pos.paletteW * self.cte, pos.paletteH * self.cte + 1)
            self.palette.repaint()
            self.brushWidget.setGeometry((pos.paletteX + pos.space) * self.cte,  \
                                             pos.paletteY * self.cte, \
                                             pos.paletteW * self.cte, \
                                             (pos.paletteH * self.cte) + 1)
            self.brushWidget.repaint()
            self.screen.image = self.screen.image.scaled(Screen.width * self.cte, \
                                                           Screen.height * self.cte)
            self.screen.setGeometry(0, 0, Screen.width * self.cte, Screen.height * self.cte)
            self.screen.repaint()

    def repaintAll(self, flag):
        self.board.recolor(flag)
        self.board.repaint()
        self.palette.repaint()
        self.brushWidget.repaint()
        self.screen.recolor()
        self.screen.repaint()

class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def __del__(self):
        pass

    def initUI(self):
        self.main = MainWidget(self)
        self.resize(win.width, win.height)
        self.setWindowTitle(win.title)
        self.setCentralWidget(self.main)
        self.center()

        self.statusBar().showMessage('Have fun!')

        fileMenu = self.menuBar().addMenu('&File')
        toolbar = self.addToolBar('Tools')
        toolbar.setIconSize(QtCore.QSize(16, 16))

        self.menuAction('Clear', self.main.board.clearBoard, 'Ctrl+K', \
                            'Create an empty file.', 'pix/clear.png', fileMenu, toolbar)
        self.menuAction('Save as', self.main.board.saveAs, 'Ctrl+S', \
                            'Save the current document.', 'pix/save.png', fileMenu, toolbar)
        self.menuAction('Exit', self.close, 'Ctrl+Q', \
                            'Exit the application, unsaved data will be lost.', 'pix/exit.png', fileMenu, toolbar)

        self.setStyleSheet("MainWindow {background-color: #C1C3C5;}")
        self.setMinimumSize(win.width, win.height)
        self.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Right:
            self.main.pal = (self.main.pal + 1) % 12
            self.main.repaintAll(True)
        if event.key() == QtCore.Qt.Key_Left:
            self.main.pal -= 1
            if self.main.pal == -1:
                self.main.pal = 11
            self.main.repaintAll(False)

    def menuAction(self, label, func, shortcut = None, tip = None, icon = None, menu = None, bar = None):
        if icon:
            ret = QtGui.QAction(QtGui.QIcon(icon), label, self)
        else:
            ret = QtGui.QAction(label, self)
        ret.setShortcut(shortcut)
        ret.setStatusTip(tip)
        ret.triggered.connect(func)
        if (menu):
            menu.addAction(ret)
        if (bar):
            bar.addAction(ret)

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def main():
    app = QtGui.QApplication(sys.argv)
    pyx = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

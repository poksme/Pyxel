# -*- coding: iso-8859-1 -*-

import sys
from PyQt4 import QtGui, QtCore

## Cr�ation de la fen�tre principale.
class Frame(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.resize(600,500)

        self.button = QtGui.QPushButton ("Hello", self)
        ## Cr�ation de l'objet self.animate issu de QPropertyAnimation.
        ## Nous passons en argument le widget qui sera � animer et la propri�t� que nous allons animer
        self.animate = QtCore.QPropertyAnimation(self.button, "geometry")
        ## Nous rentrons le d�lai de l'animation en ms
        self.animate.setDuration(800)
        ## Nous indiquons les propri�t�s de d�part
        self.animate.setStartValue(QtCore.QRect(125, 0, 100, 30))
        ## Puis les propri�t�s de fin
        self.animate.setEndValue(QtCore.QRect(125, 250, 300, 30))
        ## Et enfin nous d�marrons l'animation
        self.animate.start()


app = QtGui.QApplication(sys.argv)
frame = Frame()
frame.show()
sys.exit(app.exec_())

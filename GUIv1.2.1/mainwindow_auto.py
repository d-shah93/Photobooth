# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Sun Oct  1 14:32:25 2017
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(794, 517)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.Picbtn = QtWidgets.QPushButton(self.centralWidget)
        self.Picbtn.setGeometry(QtCore.QRect(300, 170, 131, 61))
        self.Picbtn.setStyleSheet("QPushButton{\n"
"background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 white, stop: 1 grey);\n"
"border-style: wavy;\n"
"border-color: black;\n"
"border-width: 5px;\n"
"border-radius: 10px;\n"
"}")
        self.Picbtn.setObjectName("Picbtn")
        self.Resbox = QtWidgets.QComboBox(self.centralWidget)
        self.Resbox.setGeometry(QtCore.QRect(80, 50, 131, 51))
        self.Resbox.setObjectName("Resbox")
        self.Resbox.addItem("")
        self.Resbox.addItem("")
        self.Resbox.addItem("")
        self.Resbox.addItem("")
        self.Resbox.addItem("")
        self.Resbox.addItem("")
        self.EntrBtn = QtWidgets.QPushButton(self.centralWidget)
        self.EntrBtn.setGeometry(QtCore.QRect(540, 90, 80, 23))
        self.EntrBtn.setObjectName("EntrBtn")
        self.browseBtn = QtWidgets.QPushButton(self.centralWidget)
        self.browseBtn.setGeometry(QtCore.QRect(80, 330, 131, 41))
        self.browseBtn.setObjectName("browseBtn")
        self.Delay = QtWidgets.QLineEdit(self.centralWidget)
        self.Delay.setGeometry(QtCore.QRect(530, 340, 113, 23))
        self.Delay.setObjectName("Delay")
        self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4.setGeometry(QtCore.QRect(540, 320, 201, 21))
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 794, 20))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Picbtn.setText(_translate("MainWindow", "Picture Button"))
        self.Resbox.setItemText(0, _translate("MainWindow", "500x480"))
        self.Resbox.setItemText(1, _translate("MainWindow", "720x480"))
        self.Resbox.setItemText(2, _translate("MainWindow", "720x576"))
        self.Resbox.setItemText(3, _translate("MainWindow", "1280x720"))
        self.Resbox.setItemText(4, _translate("MainWindow", "1440x1080"))
        self.Resbox.setItemText(5, _translate("MainWindow", "1920x1080"))
        self.EntrBtn.setText(_translate("MainWindow", "Enter"))
        self.browseBtn.setText(_translate("MainWindow", "Browse .PNG"))
        self.label_4.setText(_translate("MainWindow", "Delay in Seconds"))


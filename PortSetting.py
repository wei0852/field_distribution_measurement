# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\PortSetting.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(515, 421)
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(350, 330, 151, 81))
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 330, 72, 21))
        self.label.setObjectName("label")
        self.com_senser = QtWidgets.QLineEdit(Dialog)
        self.com_senser.setGeometry(QtCore.QRect(90, 330, 171, 20))
        self.com_senser.setObjectName("com_senser")
        self.apply_sensor = QtWidgets.QPushButton(Dialog)
        self.apply_sensor.setGeometry(QtCore.QRect(270, 330, 75, 23))
        self.apply_sensor.setObjectName("apply_sensor")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 360, 48, 21))
        self.label_2.setObjectName("label_2")
        self.com_motor = QtWidgets.QLineEdit(Dialog)
        self.com_motor.setGeometry(QtCore.QRect(90, 360, 171, 20))
        self.com_motor.setObjectName("com_motor")
        self.apply_motor = QtWidgets.QPushButton(Dialog)
        self.apply_motor.setGeometry(QtCore.QRect(270, 360, 75, 23))
        self.apply_motor.setObjectName("apply_motor")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 390, 60, 21))
        self.label_3.setObjectName("label_3")
        self.com_na = QtWidgets.QLineEdit(Dialog)
        self.com_na.setGeometry(QtCore.QRect(90, 390, 171, 20))
        self.com_na.setObjectName("com_na")
        self.apply_NA = QtWidgets.QPushButton(Dialog)
        self.apply_NA.setGeometry(QtCore.QRect(270, 390, 75, 23))
        self.apply_NA.setObjectName("apply_NA")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 9, 401, 121))
        self.label_4.setObjectName("label_4")
        self.current_comports = QtWidgets.QTextBrowser(Dialog)
        self.current_comports.setGeometry(QtCore.QRect(10, 140, 491, 181))
        self.current_comports.setObjectName("current_comports")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "设置串口"))
        self.label.setText(_translate("Dialog", "温湿度传感器"))
        self.apply_sensor.setText(_translate("Dialog", "应用并检验"))
        self.label_2.setText(_translate("Dialog", "步进电机"))
        self.apply_motor.setText(_translate("Dialog", "应用并检验"))
        self.label_3.setText(_translate("Dialog", "网络分析仪"))
        self.apply_NA.setText(_translate("Dialog", "应用并检验"))
        self.label_4.setText(_translate("Dialog", "<html><head/><body><p>以下是检测到的串口和仪器：在下方填入相应串口并应用</p><p>置空则为自动选择</p><p>例如：COM1</p><p>USB0::0x0957::0x0D09::MY46110247::INSTR</p><p>框内默认值是当前应用的串口(如果有) </p></body></html>"))


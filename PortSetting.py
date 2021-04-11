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
        Dialog.resize(303, 390)
        self.formLayout = QtWidgets.QFormLayout(Dialog)
        self.formLayout.setObjectName("formLayout")
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setObjectName("textBrowser")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.textBrowser)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label)
        self.com_senser = QtWidgets.QLineEdit(Dialog)
        self.com_senser.setObjectName("com_senser")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.com_senser)
        self.apply_sensor = QtWidgets.QPushButton(Dialog)
        self.apply_sensor.setObjectName("apply_sensor")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.apply_sensor)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.com_motor = QtWidgets.QLineEdit(Dialog)
        self.com_motor.setObjectName("com_motor")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.com_motor)
        self.apply_motor = QtWidgets.QPushButton(Dialog)
        self.apply_motor.setObjectName("apply_motor")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.apply_motor)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.com_na = QtWidgets.QLineEdit(Dialog)
        self.com_na.setObjectName("com_na")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.com_na)
        self.apply_NA = QtWidgets.QPushButton(Dialog)
        self.apply_NA.setObjectName("apply_NA")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.apply_NA)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_4)

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
        self.label_4.setText(_translate("Dialog", "<html><head/><body><p>如果自动连接串口出错，</p><p>可以在此处设置串口，可以在</p><p align=\"center\">&quot;此电脑&gt;属性&gt;设备管理器&quot;</p><p>中查看串口，然后在下面填入相应串口</p></body></html>"))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\FieldMeasurement.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 584)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 100, 747, 81))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 4, 1, 1)
        self.time_step = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.time_step.setMaxLength(15)
        self.time_step.setObjectName("time_step")
        self.gridLayout.addWidget(self.time_step, 2, 5, 1, 1)
        self.actual_frequency = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.actual_frequency.setReadOnly(True)
        self.actual_frequency.setObjectName("actual_frequency")
        self.gridLayout.addWidget(self.actual_frequency, 2, 3, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 1)
        self.frequency = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.frequency.setObjectName("frequency")
        self.gridLayout.addWidget(self.frequency, 2, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 2, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.measure_t_once = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.measure_t_once.setObjectName("measure_t_once")
        self.gridLayout_2.addWidget(self.measure_t_once, 1, 1, 1, 1)
        self.typein_t = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.typein_t.setObjectName("typein_t")
        self.gridLayout_2.addWidget(self.typein_t, 1, 3, 1, 1)
        self.measure_t_repeatedly = QtWidgets.QRadioButton(self.gridLayoutWidget)
        self.measure_t_repeatedly.setObjectName("measure_t_repeatedly")
        self.gridLayout_2.addWidget(self.measure_t_repeatedly, 1, 2, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 2, 1, 1)
        self.temperature = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.temperature.setReadOnly(False)
        self.temperature.setObjectName("temperature")
        self.gridLayout.addWidget(self.temperature, 0, 3, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 4, 1, 1)
        self.humidity = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.humidity.setReadOnly(False)
        self.humidity.setObjectName("humidity")
        self.gridLayout.addWidget(self.humidity, 0, 5, 1, 1)
        self.graphicsView = PlotWidget(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(30, 230, 461, 301))
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(580, 230, 151, 161))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.start_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.start_button.setObjectName("start_button")
        self.verticalLayout.addWidget(self.start_button)
        self.stop_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.stop_button.setObjectName("stop_button")
        self.verticalLayout.addWidget(self.stop_button)
        self.process_data = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.process_data.setObjectName("process_data")
        self.verticalLayout.addWidget(self.process_data)
        self.run_information = QtWidgets.QTextBrowser(self.centralwidget)
        self.run_information.setGeometry(QtCore.QRect(520, 410, 261, 121))
        self.run_information.setObjectName("run_information")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(50, 190, 71, 21))
        self.label_10.setObjectName("label_10")
        self.save_directory = QtWidgets.QTextBrowser(self.centralwidget)
        self.save_directory.setGeometry(QtCore.QRect(130, 190, 541, 21))
        self.save_directory.setObjectName("save_directory")
        self.change_directory = QtWidgets.QPushButton(self.centralwidget)
        self.change_directory.setGeometry(QtCore.QRect(680, 190, 75, 21))
        self.change_directory.setObjectName("change_directory")
        self.measurement_strategy = QtWidgets.QTabWidget(self.centralwidget)
        self.measurement_strategy.setGeometry(QtCore.QRect(30, 30, 351, 61))
        self.measurement_strategy.setObjectName("measurement_strategy")
        self.longitudinal = QtWidgets.QWidget()
        self.longitudinal.setObjectName("longitudinal")
        self.total_length = QtWidgets.QLineEdit(self.longitudinal)
        self.total_length.setGeometry(QtCore.QRect(90, 10, 81, 21))
        self.total_length.setMaxLength(15)
        self.total_length.setObjectName("total_length")
        self.label = QtWidgets.QLabel(self.longitudinal)
        self.label.setGeometry(QtCore.QRect(10, 10, 78, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.longitudinal)
        self.label_2.setGeometry(QtCore.QRect(190, 10, 78, 20))
        self.label_2.setObjectName("label_2")
        self.length_step = QtWidgets.QLineEdit(self.longitudinal)
        self.length_step.setGeometry(QtCore.QRect(270, 10, 61, 20))
        self.length_step.setMaxLength(15)
        self.length_step.setObjectName("length_step")
        self.measurement_strategy.addTab(self.longitudinal, "")
        self.angular = QtWidgets.QWidget()
        self.angular.setObjectName("angular")
        self.label_11 = QtWidgets.QLabel(self.angular)
        self.label_11.setGeometry(QtCore.QRect(50, 10, 54, 21))
        self.label_11.setObjectName("label_11")
        self.num_of_mea = QtWidgets.QLineEdit(self.angular)
        self.num_of_mea.setGeometry(QtCore.QRect(170, 10, 113, 20))
        self.num_of_mea.setObjectName("num_of_mea")
        self.measurement_strategy.addTab(self.angular, "")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(400, 30, 101, 21))
        self.label_4.setObjectName("label_4")
        self.NA_state = QtWidgets.QLineEdit(self.centralwidget)
        self.NA_state.setGeometry(QtCore.QRect(400, 60, 161, 20))
        self.NA_state.setObjectName("NA_state")
        self.na_average_facotr = QtWidgets.QSpinBox(self.centralwidget)
        self.na_average_facotr.setGeometry(QtCore.QRect(740, 60, 42, 22))
        self.na_average_facotr.setObjectName("na_average_facotr")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(710, 30, 71, 20))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(610, 30, 54, 21))
        self.label_13.setObjectName("label_13")
        self.multi_measure = QtWidgets.QSpinBox(self.centralwidget)
        self.multi_measure.setGeometry(QtCore.QRect(610, 60, 42, 22))
        self.multi_measure.setObjectName("multi_measure")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menu)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.auto_find_com = QtWidgets.QAction(MainWindow)
        self.auto_find_com.setObjectName("auto_find_com")
        self.setting_port = QtWidgets.QAction(MainWindow)
        self.setting_port.setObjectName("setting_port")
        self.open_file = QtWidgets.QAction(MainWindow)
        self.open_file.setObjectName("open_file")
        self.save_file = QtWidgets.QAction(MainWindow)
        self.save_file.setObjectName("save_file")
        self.menuFile.addAction(self.open_file)
        self.menuFile.addAction(self.save_file)
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menu_2.addAction(self.auto_find_com)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.setting_port)
        self.menu.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.measurement_strategy.setCurrentIndex(0)
        self.actionQuit.triggered.connect(MainWindow.close)
        self.measure_t_once.clicked.connect(self.temperature.hide)
        self.measure_t_once.clicked.connect(self.humidity.hide)
        self.typein_t.clicked.connect(self.temperature.show)
        self.typein_t.clicked.connect(self.humidity.show)
        self.measure_t_repeatedly.clicked.connect(self.temperature.hide)
        self.measure_t_repeatedly.clicked.connect(self.humidity.hide)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "??????????????????????????????"))
        self.label_3.setText(_translate("MainWindow", "????????????(s)"))
        self.label_8.setText(_translate("MainWindow", "????????????(MHz)"))
        self.label_9.setText(_translate("MainWindow", "????????????(MHz)"))
        self.label_5.setText(_translate("MainWindow", "???????????????"))
        self.measure_t_once.setText(_translate("MainWindow", "????????????"))
        self.typein_t.setText(_translate("MainWindow", "????????????"))
        self.measure_t_repeatedly.setText(_translate("MainWindow", "????????????"))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\">??????(???)</p></body></html>"))
        self.label_7.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\">??????(%)</p></body></html>"))
        self.start_button.setText(_translate("MainWindow", "??????"))
        self.stop_button.setText(_translate("MainWindow", "??????"))
        self.process_data.setText(_translate("MainWindow", "????????????"))
        self.label_10.setText(_translate("MainWindow", "??????????????????"))
        self.change_directory.setText(_translate("MainWindow", "????????????"))
        self.measurement_strategy.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>??????</p></body></html>"))
        self.label.setText(_translate("MainWindow", "????????????(mm)"))
        self.label_2.setText(_translate("MainWindow", "????????????(mm)"))
        self.measurement_strategy.setTabText(self.measurement_strategy.indexOf(self.longitudinal), _translate("MainWindow", "?????????????????????"))
        self.label_11.setText(_translate("MainWindow", "????????????"))
        self.measurement_strategy.setTabText(self.measurement_strategy.indexOf(self.angular), _translate("MainWindow", "?????????????????????"))
        self.label_4.setText(_translate("MainWindow", "????????????(??????)"))
        self.label_12.setText(_translate("MainWindow", "??????????????????"))
        self.label_13.setText(_translate("MainWindow", "????????????"))
        self.menuFile.setTitle(_translate("MainWindow", "??????"))
        self.menuHelp.setTitle(_translate("MainWindow", "??????"))
        self.menu.setTitle(_translate("MainWindow", "??????"))
        self.menu_2.setTitle(_translate("MainWindow", "????????????"))
        self.actionAbout.setText(_translate("MainWindow", "??????"))
        self.actionAbout.setShortcut(_translate("MainWindow", "Ctrl+H"))
        self.actionQuit.setText(_translate("MainWindow", "??????"))
        self.actionQuit.setIconText(_translate("MainWindow", "??????"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.auto_find_com.setText(_translate("MainWindow", "default"))
        self.setting_port.setText(_translate("MainWindow", "????????????"))
        self.open_file.setText(_translate("MainWindow", "??????"))
        self.save_file.setText(_translate("MainWindow", "??????"))

from pyqtgraph import PlotWidget

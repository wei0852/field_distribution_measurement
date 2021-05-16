import sys
from os import environ
from threading import Thread, Event
from time import sleep
import pyqtgraph as pg
from serial.tools import list_ports
from serial import Serial
from pyvisa import ResourceManager
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QDialog
from math import sqrt

import FieldMeasurement
import PortSetting
from PyQt5.QtGui import QTextCursor

import input
from measurementCore import Sensor, StepMotor, NetworkAnalyzer

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


def get_measure_par(input_object):
    """get input parameters on GUI"""
    input_object.measurement_strategy = ui.measurement_strategy.currentIndex()
    input_object.len_total = ui.total_length.text()
    input_object.frequency = ui.frequency.text()
    input_object.num_of_mea = ui.num_of_mea.text()
    input_object.len_step = ui.length_step.text()
    input_object.time_step = ui.time_step.text()
    input_object.temperature = ui.temperature.text()
    input_object.humidity = ui.humidity.text()
    input_object.na_average_factor = ui.na_average_facotr.value()
    input_object.multi_measure = ui.multi_measure.value()
    if ui.NA_state.text().strip() != '':
        input_object.na_state = ui.NA_state.text().strip()
    else:
        input_object.na_state = None


def change_directory():
    input_parameters.directory = QFileDialog.getExistingDirectory(MainWindow, '选择测量数据保存位置', default_path)
    ui.save_directory.setText(input_parameters.directory)


class MeasureThread(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.__running = Event()
        self.__running.set()
        self.__waiting = Event()
        self.__waiting.clear()
        self.setDaemon(True)

    def run(self):
        """measuring"""
        try:
            measurement = input_parameters.generate_measurement()
            ui.actual_frequency.setText(str(measurement.f_r / 1e6))
            ui.run_information.append("开始测量...")
            sleep(0.1)  #
            ui.run_information.moveCursor(QTextCursor.End)
            for plot_x, plot_y in measurement.run():
                plot_data.update(plot_x, plot_y)
                if not self.__running.isSet():
                    measurement.save_data(input_parameters.directory)
                    ui.run_information.append("测量终止！！！！")
                    sleep(0.1)
                    ui.run_information.moveCursor(QTextCursor.End)
                    input_parameters.close_ser()
                    measurement_thread.stop()
                    return -1
            measurement_thread.stop()
            input_parameters.close_ser()
            measurement.save_data(input_parameters.directory)
            ui.run_information.append("测量完成！！！\n--------------")
            sleep(0.3)
            ui.run_information.moveCursor(QTextCursor.End)
        except Exception as e:
            input_parameters.close_ser()
            ui.run_information.append("Error:\n" + str(e))
            sleep(0.1)  #
            ui.run_information.moveCursor(QTextCursor.End)

    def stop(self):
        self.__running.clear()


class PlotData(object):
    def __init__(self):
        self.data = []
        self.s = []
        self.curve = None
        self.scatter = None

    def update(self, position, field):
        """update plot data"""
        self.data.append(field)
        self.s.append(position)
        # self.curve.setData(self.s, self.data, pen=None, symbol='o')
        self.curve.setData(self.s, self.data)
        # self.scatter.addPoints(self.s, self.data)

    def reset(self):
        ui.graphicsView.clear()
        self.curve = ui.graphicsView.plot([0], [0], pen='k', symbol='o', symbolSize=5)
        ui.graphicsView.showGrid(x=True, y=True)
        # self.scatter = pg.ScatterPlotItem(size=2, brush=pg.mkBrush(50, 50, 50))
        # ui.graphicsView.addItem(self.scatter)
        self.data = []
        self.s = []
        if input_parameters.measurement_strategy == 0:
            ui.graphicsView.setTitle('谐振腔轴向场分布测量')
            ui.graphicsView.setLabel('left', 'Δ_f', 'Hz')
            ui.graphicsView.setLabel('bottom', '位置', 'mm')
        elif input_parameters.measurement_strategy == 1:
            ui.graphicsView.setTitle('谐振腔横向向场分布测量')
            ui.graphicsView.setLabel('left', 'Δ_f', 'Hz')
            ui.graphicsView.setLabel('bottom', '位置', 'degree')

    def normalize(self):
        if not self.data:
            return
        data_range = max(self.data) - min(self.data)
        min_data = min(self.data)
        if data_range == 0:
            normalized_data = [0 for _ in self.data]
        else:
            normalized_data = [sqrt((i - min_data) / data_range) for i in self.data]
        ui.graphicsView.setLabel('left', '归一化场强', '')
        self.scatter.clear()
        self.scatter.addPoints(self.s, normalized_data)


class MeasurementThreadManage(object):
    """manage measurement thread, generate new thread, and """

    def __init__(self):
        self.measurement_thread = None
        self.started = False

    def start(self):
        if not self.started:
            ui.run_information.setText('检查输入参数...')
            sleep(0.1)  # 给信息框一点反应时间
            ui.run_information.moveCursor(QTextCursor.End)
            try:
                get_measure_par(input_parameters)
                input_parameters.check_data()
                ui.run_information.append(str(input_parameters))
                sleep(0.1)
                ui.run_information.moveCursor(QTextCursor.End)
                plot_data.reset()
            except input.InputError as e:
                input_parameters.close_ser()
                missing_parameters(e.reason)
                return -1
            self.measurement_thread = MeasureThread('measurement_thread')
            self.started = True
            self.measurement_thread.start()

    def stop(self):
        if self.started:
            self.measurement_thread.stop()
            self.started = False


def missing_parameters(reason):
    QMessageBox.critical(MainWindow, '输入参数错误', str(reason))


def about_information():
    text = '谐振腔场分布测量程序\n步进电机：MOONS STM24SF-3AE，网分型号：Agilent E5071C\n' \
           '\nhttps://github.com/wei0852/field_distribution_measurement'
    QMessageBox.about(MainWindow, '关于', text)


def show_setting_port():
    """open Dialog window to set ports manually"""

    def verify_sensor():
        sensor_com = ui_setting_port.com_senser.text()
        try:
            ui_setting_port.textBrowser.setText(f'传感器串口： {sensor_com}')
            ser = Serial(sensor_com, 9600, timeout=2)
            temp_sensor = Sensor(ser)
            ui_setting_port.textBrowser.append(str(temp_sensor.current_t_rh))
            ser.close()
            input_parameters.sensor_comp = sensor_com
        except Exception as e:
            ui_setting_port.textBrowser.append(str(e))

    def verify_motor():
        motor_com = ui_setting_port.com_motor.text()
        try:
            ui_setting_port.textBrowser.setText(f'步进电机串口： {motor_com}')
            ser = Serial(motor_com, 9600, timeout=0.2)
            temp_sensor = StepMotor(ser)
            temp_sensor.move_forward()
            ser.close()
            input_parameters.motor_comp = motor_com
        except Exception as e:
            ui_setting_port.textBrowser.append(str(e))

    def verify_network_analyzer():
        na_identifier = ui_setting_port.com_na.text()
        try:
            ui_setting_port.textBrowser.setText(f'网分： {na_identifier}')
            ser = input_parameters.visa_rm.open_resource(na_identifier)
            NetworkAnalyzer(ser)
            ui_setting_port.textBrowser.append('没毛病嗷\n┗|｀O′|┛ 嗷~~')
            ser.close()
            input_parameters.NA_identifier = na_identifier
        except Exception as e:
            ui_setting_port.textBrowser.append(str(e))

    setting_port = QDialog()
    ui_setting_port = PortSetting.Ui_Dialog()
    ui_setting_port.setupUi(setting_port)
    ports = list(list_ports.comports())
    text = '        当前已连接串口：\n'
    for p in ports:
        text += f'{p[1]}\n'
    text += '        仪器\n'
    for p in ResourceManager().list_resources():
        text += f'{p}\n'
    ui_setting_port.current_comports.setText(text)
    ui_setting_port.com_motor.setText(input_parameters.motor_comp)
    ui_setting_port.com_senser.setText(input_parameters.sensor_comp)
    ui_setting_port.com_na.setText(input_parameters.NA_identifier)
    ui_setting_port.apply_sensor.clicked.connect(verify_sensor)
    ui_setting_port.apply_motor.clicked.connect(verify_motor)
    ui_setting_port.apply_NA.clicked.connect(verify_network_analyzer)
    setting_port.exec_()


def open_file():
    """select input file and show its data"""

    file_name, file_type = QFileDialog.getOpenFileName(MainWindow, '选择文件', default_path, 'txt(*.txt)')
    if file_name == '':
        return
    temp_input = input.read_file(file_name)
    try:
        if temp_input.measurement_strategy == '0':
            ui.measurement_strategy.setCurrentIndex(0)
            ui.total_length.setText(temp_input.len_total)
            ui.length_step.setText(temp_input.len_step)
        elif temp_input.measurement_strategy == '1':
            ui.measurement_strategy.setCurrentIndex(1)
            ui.num_of_mea.setText(temp_input.num_of_mea)
        ui.frequency.setText(temp_input.frequency)
        ui.time_step.setText(temp_input.time_step)
        ui.na_average_facotr.setValue(int(temp_input.na_average_factor))
        ui.multi_measure.setValue(int(temp_input.multi_measure))
        ui.save_directory.setText(temp_input.directory)
        input_parameters.directory = temp_input.directory
        if temp_input.access_sensor_times == '0':
            ui.typein_t.setChecked(True)
            input_parameters.access_sensor_times = 0
            ui.temperature.setText(temp_input.temperature)
            ui.humidity.setText(temp_input.humidity)
        elif temp_input.access_sensor_times == '1':
            ui.measure_t_once.setChecked(True)
            input_parameters.access_sensor_times = 1
        elif temp_input.access_sensor_times == '2':
            ui.measure_t_repeatedly.setChecked(True)
            input_parameters.access_sensor_times = 2
        if temp_input.na_state is not None:
            ui.NA_state.setText(temp_input.na_state)
        input_parameters.motor_comp = temp_input.motor_comp
        input_parameters.sensor_comp = temp_input.sensor_comp
        input_parameters.NA_identifier = temp_input.NA_identifier
    except Exception:
        missing_parameters('文件格式错误，请补充相应数据')


def save_file():
    """save input file, not the measurement result."""

    file_name, ok = QFileDialog.getSaveFileName(MainWindow, '保存输入文件', default_path, 'txt(*.txt)')
    try:
        get_measure_par(input_parameters)
        input_parameters.check_data()
        input_parameters.close_ser()
    except Exception as e:
        QMessageBox.critical(MainWindow, '!!!', f'保存失败，缺少必要参数:\n {e}')
        return
    if file_name != '':
        input_parameters.save_input_file(file_name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = FieldMeasurement.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    default_path = environ['USERPROFILE'] + '\\Documents\\field_distribution_measurement'
    input_parameters = input.InputParameter()
    measurement_thread = MeasurementThreadManage()
    plot_data = PlotData()
    ui.start_button.clicked.connect(measurement_thread.start)
    ui.na_average_facotr.setMinimum(1)
    ui.na_average_facotr.setMaximum(999)
    ui.na_average_facotr.setValue(4)
    ui.multi_measure.setMinimum(1)
    ui.multi_measure.setMaximum(15)
    ui.stop_button.clicked.connect(measurement_thread.stop)
    ui.process_data.clicked.connect(plot_data.normalize)
    ui.typein_t.clicked.connect(input_parameters.manual_measure_temperature_humidity)
    ui.measure_t_once.clicked.connect(input_parameters.access_sensor_once)
    ui.measure_t_repeatedly.clicked.connect(input_parameters.access_sensor_repeat)
    ui.auto_find_com.triggered.connect(input_parameters.set_auto_find_comp)
    ui.change_directory.clicked.connect(change_directory)
    ui.actionAbout.triggered.connect(about_information)
    ui.setting_port.triggered.connect(show_setting_port)
    ui.open_file.triggered.connect(open_file)
    ui.save_file.triggered.connect(save_file)
    sys.exit(app.exec_())

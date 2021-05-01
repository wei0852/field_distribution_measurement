import sys
import threading
import time
import serial.tools.list_ports
import pyqtgraph as pg
import pyvisa
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QDialog

import FieldMeasurement
import PortSetting
from PyQt5.QtGui import QTextCursor
from measurementCore import LongitudinalMeasurement, Sensor, StepMotor, TestMeasurement, NetworkAnalyzer

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class InputError(Exception):
    def __init__(self, reason):
        self.reason = reason


class InputParameter(object):
    def __init__(self):
        self.measurement_strategy = None
        self.len_total = None
        self.len_step = None
        self.time_step = None
        self.frequency = None
        self.temperature = None
        self.humidity = None
        self.access_sensor_times = None
        self.directory = "./data"
        self.sensor_comp = None
        self.motor_comp = None
        self.network_analysis_resource = None
        self.auto_find_comp = True
        self.sensor_ser = None
        self.motor_ser = None
        self.visa_rm = pyvisa.ResourceManager()
        self.motor = None
        self.sensor = None
        self.NA = None
        self.NA_identifier = None
        ui.save_directory.setText(self.directory)

    def check_data(self):
        """check input parameters, """
        if self.len_total == '':
            raise InputError('缺少腔体长度')
        self.len_total = float(self.len_total)
        if self.len_step == '':
            raise InputError('缺少运动步长')
        self.len_step = float(self.len_step)
        if self.len_step * self.len_total <= 0:
            raise InputError('总长度和步长符号须一致，符号表示反向')
        if self.time_step == '':
            raise InputError('缺少等待时间')
        self.time_step = float(self.time_step)
        if self.time_step < 1:
            raise InputError('至少等1s')
        self.time_step = self.time_step - 0.2  # minus the time to read the result of step motor
        if self.frequency == '':
            raise InputError('缺少真空频率')
        self.frequency = float(self.frequency) * 1e6
        ui.run_information.append("检查串口连接情况...")
        time.sleep(0.1)  #
        ui.run_information.moveCursor(QTextCursor.End)
        if self.access_sensor_times is None or self.access_sensor_times == 0:
            if self.temperature == '':
                raise InputError('缺少温度数据')
            if self.humidity == '':
                raise InputError('缺少湿度数据')
            self.temperature = float(self.temperature)
            self.humidity = float(self.humidity) / 100
            self.access_sensor_times = 0
        else:
            self.temperature = ''
            self.humidity = ''
            if self.sensor_comp is None:
                try:
                    port_list = list(serial.tools.list_ports.comports())
                    self.sensor_comp = port_list[1][0]
                except IndexError:
                    raise InputError('检查串口连接情况')
            try:
                self.sensor_ser = serial.Serial(self.sensor_comp, 9600, timeout=2)
                self.sensor = Sensor(self.sensor_ser)
            except Exception as e:
                raise InputError(str(e))
            self.access_sensor_times = float(self.access_sensor_times)
            if self.access_sensor_times == 2 and self.time_step < 2.5:
                raise InputError('使用传感器，需要更多等待时间')
        # Step Motor
        if self.motor_comp is None and self.measurement_strategy != 1:
            try:
                self.motor_comp = list(serial.tools.list_ports.comports())[0][0]
            except Exception as e:
                raise InputError('检查串口连接情况\n' + str(e))
        try:
            self.motor_ser = serial.Serial(self.motor_comp, 9600, timeout=0.2)
            self.motor = StepMotor(self.motor_ser, self.len_step)
        except Exception as e:
            raise InputError('检查串口连接情况\n' + str(e))
        # Network Analyzer
        if self.network_analysis_resource is None and self.measurement_strategy != 1:
            try:
                self.NA_identifier = self.visa_rm.list_resources()[0]
            except Exception as e:
                raise InputError('检查网分连接情况\n' + str(e))
        try:
            self.network_analysis_resource = self.visa_rm.open_resource(self.NA_identifier)
            self.NA = NetworkAnalyzer(self.network_analysis_resource)
        except Exception as e:
            raise InputError('检查网分连接情况\n' + str(e))

    def get_measure_par(self):
        """get input parameters on GUI"""
        self.measurement_strategy = ui.measurement_stratety.currentIndex()
        self.len_total = ui.total_length.text()
        self.frequency = ui.frequency.text()
        self.len_step = ui.length_step.text()
        self.time_step = ui.time_step.text()
        self.temperature = ui.temperature.text()
        self.humidity = ui.humidity.text()
        ui.run_information.append(str(self))
        time.sleep(0.2)
        ui.run_information.append('----------------\n')
        ui.run_information.moveCursor(QTextCursor.End)
        self.check_data()

    def pass_parameters(self, measurement_object):
        """pass input parameters to measurement object"""
        measurement_object.len_total = self.len_total
        measurement_object.f0 = self.frequency
        measurement_object.len_step = self.len_step
        measurement_object.time_step = self.time_step
        measurement_object.temperature = self.temperature
        measurement_object.humidity = self.humidity
        measurement_object.access_sensor_times = self.access_sensor_times
        measurement_object.motor = self.motor
        measurement_object.sensor = self.sensor
        measurement_object.network_analyzer = self.NA

    def access_sensor_once(self):
        self.access_sensor_times = 1

    def access_sensor_repeat(self):
        self.access_sensor_times = 2

    def manual_measure_temperature_humidity(self):
        self.access_sensor_times = 0

    def change_directory(self):
        self.directory = QFileDialog.getExistingDirectory(MainWindow)
        ui.save_directory.setText(self.directory)

    def set_auto_find_comp(self):
        self.sensor_comp = None
        self.motor_comp = None
        self.network_analysis_resource = None

    def close_ser(self):
        if isinstance(self.sensor_ser, serial.Serial):
            self.sensor_ser.close()
        if isinstance(self.motor_ser, serial.Serial):
            self.motor_ser.close()
        if isinstance(self.network_analysis_resource, pyvisa.Resource):
            self.network_analysis_resource.close()

    def generate_measurement(self):
        """generate different measurement according to different strategy"""
        if self.measurement_strategy == 0:
            m1 = LongitudinalMeasurement()
            self.pass_parameters(m1)
            return m1
        elif self.measurement_strategy == 1:
            m1 = TestMeasurement()
            self.pass_parameters(m1)
            return m1

    def __str__(self):
        text = ''
        text += ('\n腔体长度 = ' + str(self.len_total) + ' mm')
        text += ("\n运动步长 = " + str(self.len_step) + ' mm')
        text += ("\n等待时间 = " + str(self.time_step) + ' s')
        text += ("\n真空频率 = " + str(self.frequency) + 'MHz')
        if self.access_sensor_times == 0 or self.access_sensor_times is None:
            text += ("\n温度 = " + str(self.temperature) + '℃')
            text += ("\n湿度 = " + str(self.humidity) + '%\n')
        else:
            text += "\n温湿度数据由传感器提供\n"
        return text


class MeasureThread(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.__running = threading.Event()
        self.__running.set()
        self.__waiting = threading.Event()
        self.__waiting.clear()
        self.setDaemon(True)

    def run(self):
        """measuring"""
        try:
            measurement = input_parameters.generate_measurement()
            ui.actual_frequency.setText(str(measurement.cal_cavity_frequency()))
            ui.run_information.append("开始测量...")
            time.sleep(0.1)  #
            ui.run_information.moveCursor(QTextCursor.End)
            current_plot = PlotData()
            for position, field in measurement.run():
                current_plot.update(position, field)
                if not self.__running.isSet():
                    measurement.save_data(input_parameters.directory)
                    ui.run_information.append("测量终止！！！！")
                    time.sleep(0.1)
                    ui.run_information.moveCursor(QTextCursor.End)
                    input_parameters.close_ser()
                    measurement_thread.stop()
                    return -1
            measurement_thread.stop()
            input_parameters.close_ser()
            measurement.save_data(input_parameters.directory)
            ui.run_information.append("测量完成！！！\n--------------")
            ui.run_information.moveCursor(QTextCursor.End)
        except Exception as e:
            ui.run_information.append("串口通信出错\n" + str(e))
            time.sleep(0.1)  #
            ui.run_information.moveCursor(QTextCursor.End)

    def stop(self):
        self.__running.clear()


class PlotData(object):
    def __init__(self):
        self.data = []
        self.s = []
        self.curve = ui.graphicsView.plot([0], [0])

    def update(self, position, field):
        self.data.append(field)
        self.s.append(position)
        self.curve.setData(self.s, self.data, pen='k')


class MeasurementThreadManage(object):
    """manage measurement thread, generate new thread, and """

    def __init__(self):
        self.measurement_thread = None
        self.started = False

    def start(self):
        if not self.started:
            ui.run_information.clear()
            time.sleep(0.1)  # 给信息框一点反应时间
            ui.graphicsView.clear()
            try:
                input_parameters.get_measure_par()
            except InputError as e:
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
    QMessageBox.about(MainWindow, '关于', '未完成')


def initialize_plot():
    ui.graphicsView.setTitle('谐振腔归一化场分布测量')
    ui.graphicsView.setLabel('left', 'Δ_f', 'Hz')
    ui.graphicsView.setLabel('bottom', '位置', 'mm')


def show_setting_port():
    def verify_sensor():
        sensor_com = ui_setting_port.com_senser.text()
        try:
            ui_setting_port.textBrowser.setText(f'传感器串口： {sensor_com}')
            ser = serial.Serial(sensor_com, 9600, timeout=2)
            temp_sensor = Sensor(ser)
            ui_setting_port.textBrowser.append(str(temp_sensor.current_t_rh))
            ser.close()
            input_parameters.sensor_comp = sensor_com
        except Exception:
            ui_setting_port.textBrowser.append('串口错误')

    def verify_motor():
        motor_com = ui_setting_port.com_motor.text()
        try:
            ui_setting_port.textBrowser.setText(f'步进电机串口： {motor_com}')
            ser = serial.Serial(motor_com, 9600, timeout=0.2)
            temp_sensor = StepMotor(ser, 10)
            temp_sensor.move_forward()
            ser.close()
            input_parameters.motor_comp = motor_com
        except Exception:
            ui_setting_port.textBrowser.append('串口错误')

    def verify_network_analyzer():
        na_resource = ui_setting_port.com_motor.text()
        try:
            ui_setting_port.textBrowser.setText(f'步进电机串口： {na_resource}')
            ser = input_parameters.visa_rm.open_resource(na_resource)
            temp_sensor = NetworkAnalyzer(ser)
            ser.close()
            input_parameters.network_analysis_resource = na_resource
        except Exception:
            ui_setting_port.textBrowser.append('串口错误')

    setting_port = QDialog()
    ui_setting_port = PortSetting.Ui_Dialog()
    ui_setting_port.setupUi(setting_port)
    ui_setting_port.apply_sensor.clicked.connect(verify_sensor)
    ui_setting_port.apply_motor.clicked.connect(verify_motor)
    ui_setting_port.apply_NA.clicked.connect(verify_network_analyzer)
    setting_port.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = FieldMeasurement.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    input_parameters = InputParameter()
    measurement_thread = MeasurementThreadManage()
    initialize_plot()
    ui.start_button.clicked.connect(measurement_thread.start)
    ui.stop_button.clicked.connect(measurement_thread.stop)
    ui.temp_typein.clicked.connect(input_parameters.manual_measure_temperature_humidity)
    ui.temp_mea_once.clicked.connect(input_parameters.access_sensor_once)
    ui.temp_mea_more.clicked.connect(input_parameters.access_sensor_repeat)
    ui.auto_find_com.triggered.connect(input_parameters.set_auto_find_comp)
    ui.change_directory.clicked.connect(input_parameters.change_directory)
    ui.actionAbout.triggered.connect(about_information)
    ui.setting_port.triggered.connect(show_setting_port)
    sys.exit(app.exec_())

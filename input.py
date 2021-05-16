from serial.tools import list_ports
from serial import Serial
from pyvisa import ResourceManager
from measurementCore import LongitudinalMeasurement, Sensor, StepMotor, NetworkAnalyzer, AngularMeasurement


class InputError(Exception):
    def __init__(self, reason):
        self.reason = reason


class InputParameter(object):
    def __init__(self):
        self.measurement_strategy = None
        self.len_total = None
        self.len_step = None
        self.num_of_mea = None
        self.time_step = None
        self.frequency = None
        self.temperature = None
        self.humidity = None
        self.access_sensor_times = None
        self.directory = None
        self.sensor_comp = None
        self.motor_comp = None
        self.network_analysis_resource = None
        self.auto_find_comp = True
        self.sensor_ser = None
        self.motor_ser = None
        self.visa_rm = ResourceManager()
        self.motor = None
        self.sensor = None
        self.NA = None
        self.NA_identifier = None
        self.na_state = None
        self.na_average_factor = None
        self.multi_measure = None

    def check_data(self):
        """check input parameters, and open serials, remember to close ser!!!"""

        if self.directory is None:
            raise InputError('请选择数据保存位置')
        try:
            self.measurement_strategy = int(self.measurement_strategy)
        except Exception:
            raise InputError('须指定测量方案')
        if self.measurement_strategy == 0:
            try:
                self.len_total = float(self.len_total)
            except Exception:
                raise InputError('缺少腔体长度')
            try:
                self.len_step = float(self.len_step)
            except Exception:
                raise InputError('缺少运动步长')
            if self.len_step * self.len_total <= 0:
                raise InputError('总长度和步长符号须一致，负号表示反向')
        elif self.measurement_strategy == 1:
            try:
                self.num_of_mea = float(self.num_of_mea)
            except Exception:
                raise InputError('请指定一周测量次数')
        try:
            self.time_step = float(self.time_step)
        except Exception:
            raise InputError('缺少等待时间')
        if self.time_step < 1:
            raise InputError('至少等1s')
        try:
            self.multi_measure = int(self.multi_measure)
        except Exception:
            raise InputError('指定测量次数')
        try:
            self.frequency = float(self.frequency)
        except Exception:
            raise InputError('缺少真空频率')
        if self.access_sensor_times is None:
            self.access_sensor_times = 0
        try:
            self.access_sensor_times = int(self.access_sensor_times)
        except Exception:
            raise InputError('设置温湿度')
        if self.access_sensor_times == 0:
            try:
                self.temperature = float(self.temperature)
            except Exception:
                raise InputError('缺少温度数据')
            try:
                self.humidity = float(self.humidity)
            except Exception:
                raise InputError('缺少湿度数据')
        else:
            if self.access_sensor_times == 2 and self.time_step < 2.5:
                raise InputError('使用传感器，需要更多等待时间')
            if self.sensor_comp is None:
                try:
                    port_list = list(list_ports.comports())
                    self.sensor_comp = port_list[1][0]
                except IndexError:
                    raise InputError('检查串口连接情况')
            try:
                self.sensor_ser = Serial(self.sensor_comp, 9600, timeout=2)
                self.sensor = Sensor(self.sensor_ser)
                [self.temperature, self.humidity] = self.sensor.current_t_rh
            except Exception as e:
                raise InputError(f'串口错误:\n{e}')
        # Step Motor
        if self.motor_comp is None:
            try:
                self.motor_comp = list(list_ports.comports())[0][0]
            except Exception as e:
                raise InputError('检查串口连接情况\n' + str(e))
        try:
            self.motor_ser = Serial(self.motor_comp, 9600, timeout=0.2)
            self.motor = StepMotor(self.motor_ser)
        except Exception as e:
            raise InputError('检查串口连接情况\n' + str(e))
        # Network Analyzer
        try:
            self.na_average_factor = int(self.na_average_factor)
        except ValueError or TypeError:
            raise InputError('网分平均因子出错')
        if self.NA_identifier is None:
            try:
                self.NA_identifier = self.visa_rm.list_resources()[0]
            except Exception as e:
                raise InputError('检查网分连接情况\n' + str(e))
        try:
            self.network_analysis_resource = self.visa_rm.open_resource(self.NA_identifier)
            self.NA = NetworkAnalyzer(self.network_analysis_resource, self.na_state, self.na_average_factor)
        except Exception as e:
            raise InputError('检查网分连接情况\n' + str(e))

    def pass_parameters(self, measurement_object):
        """pass input parameters to measurement object"""
        measurement_object.len_total = self.len_total
        measurement_object.f0 = self.frequency * 1e6
        measurement_object.num_of_measurements = self.num_of_mea
        measurement_object.len_step = self.len_step
        measurement_object.time_step = self.time_step
        measurement_object.na_average_factor = self.na_average_factor
        measurement_object.multi_measure = self.multi_measure
        measurement_object.temperature = self.temperature
        measurement_object.humidity = self.humidity / 100
        measurement_object.access_sensor_times = self.access_sensor_times
        measurement_object.motor = self.motor
        measurement_object.sensor = self.sensor
        measurement_object.network_analyzer = self.NA
        measurement_object.cal_cavity_frequency()

    def access_sensor_once(self):
        self.access_sensor_times = 1

    def access_sensor_repeat(self):
        self.access_sensor_times = 2

    def manual_measure_temperature_humidity(self):
        self.access_sensor_times = 0

    def set_auto_find_comp(self):
        self.sensor_comp = None
        self.motor_comp = None
        self.network_analysis_resource = None

    def close_ser(self):
        if isinstance(self.sensor_ser, Serial):
            self.sensor_ser.close()
        if isinstance(self.motor_ser, Serial):
            self.motor_ser.close()
        try:
            self.network_analysis_resource.close()
        except Exception:
            return

    def generate_measurement(self):
        """generate different measurement according to different strategy"""
        if self.measurement_strategy == 0:
            m1 = LongitudinalMeasurement()
            self.motor.set_distance(distance_mm=self.len_step)
            self.pass_parameters(m1)
            return m1
        elif self.measurement_strategy == 1:
            m1 = AngularMeasurement()
            self.motor.set_distance(distance=20000/self.num_of_mea)
            self.pass_parameters(m1)
            return m1

    def save_input_file(self, file_name):
        file1 = open(file_name, 'w')
        file1.write('& input parameters for field distribution measurement program\n')
        file1.write('& lines begin with \'&\' will be ignored, \n'
                    '& you don\'t have to write these lines in your input file.\n&\n&----------------------------\n&\n')
        file1.write('& measurement strategy (0 for longitudinal measurement, 1 for angular measurement)\n')
        file1.write(f'    {self.measurement_strategy}\n')
        if self.measurement_strategy == 0:
            file1.write('& total length         movement step\n')
            file1.write(f'    {self.len_total}        {self.len_step}\n')
        elif self.measurement_strategy == 1:
            file1.write('& number of measurement\n')
            file1.write(f'    {self.num_of_mea}\n')
        file1.write('& waiting time              multiple measurement time at each position (optional, default 1)\n')
        file1.write(f'    {self.time_step} {self.multi_measure}\n')
        file1.write('& vacuum frequency\n')
        file1.write(f'    {self.frequency}\n')
        file1.write('& temperature and humidity\n')
        if self.access_sensor_times == 0:
            file1.write(f'    0    {self.temperature}    {self.humidity}\n')
        else:
            file1.write(f'    {int(self.access_sensor_times)}\n')
        file1.write('& data storage directory\n')
        file1.write(f'    {self.directory}\n')
        file1.write('& sensor (0 for auto find)\n')
        if self.sensor_comp is None:
            file1.write(f'    0\n')
        else:
            file1.write(f'    {self.sensor_comp}\n')
        file1.write('& motor (0 for auto find)\n')
        if self.motor_comp is None:
            file1.write(f'    0\n')
        else:
            file1.write(f'    {self.motor_comp}\n')
        file1.write('& network analyzer (0 for auto find)\n')
        if self.NA_identifier is None:
            file1.write(f'    0\n')
        else:
            file1.write(f'    {self.NA_identifier}\n')
        file1.write('& network analyzer average factor\n')
        file1.write(f'    {self.na_average_factor}\n')
        file1.write('& network analyzer state (optional)\n')
        if self.na_state is not None:
            file1.write(f'    {self.na_state}\n')
        file1.close()

    def __str__(self):
        text = ''
        if self.measurement_strategy == 0:
            text += f'\n{"腔体长度":4} = {self.len_total:8f} mm'
            text += f"\n{'运动步长':4} = {self.len_step:8f} mm"
        elif self.measurement_strategy == 1:
            text += f"\n{'测量次数':4} = {self.num_of_mea:4f}"
        text += f"\n{'等待时间':4} = {self.time_step:8f} s"
        text += f"\n{'真空频率':4} = {self.frequency:8f} MHz"
        if self.access_sensor_times == 1 or self.access_sensor_times == 2:
            text += "\n温湿度数据由传感器提供\n"
        text += f"\n{'温度':4} = {self.temperature:8f} ℃"
        text += f"\n{'湿度':4} = {self.humidity:8f} %\n"
        return text


def read_file(file_name) -> InputParameter:
    """read data in file and generate InputParameter, the return input should be checked."""

    def next_useful_line():
        current_line = next(lines)
        temp_line = current_line.strip()
        if temp_line == '' or temp_line[0] == '&':
            current_line = next_useful_line()
        return current_line

    input_object = InputParameter()
    file1 = open(file_name)
    try:
        lines = iter(file1.readlines())
        line = next(lines)
        if line.strip() == '' or line.strip()[0] == '&':
            line = next_useful_line()
        items = line.strip().split()
        input_object.measurement_strategy = items[0]
        #
        line = next_useful_line()
        items = line.strip().split()
        if input_object.measurement_strategy == '0':
            input_object.len_total = items[0]
            input_object.len_step = items[1]
        elif input_object.measurement_strategy == '1':
            input_object.num_of_mea = items[0]
        # time step & multi_measure
        line = next_useful_line()
        items = line.strip().split()
        input_object.time_step = items[0]
        input_object.multi_measure = items[1]
        # vacuum frequency
        line = next_useful_line()
        items = line.strip().split()
        input_object.frequency = items[0]
        # temperature & humidity
        line = next_useful_line()
        items = line.strip().split()
        input_object.access_sensor_times = items[0]
        if input_object.access_sensor_times == '0':
            input_object.temperature = items[1]
            input_object.humidity = items[2]
        # directory for saving data
        line = next_useful_line()
        items = line.strip()
        input_object.directory = items
        # sensor com
        line = next_useful_line()
        items = line.strip()
        if items[0] != '0':
            input_object.sensor_comp = items
        # motor com
        line = next_useful_line()
        items = line.strip()
        if items[0] != '0':
            input_object.motor_comp = items
        line = next_useful_line()
        items = line.strip()
        if items[0] != '0':
            input_object.NA_identifier = items
        line = next_useful_line()
        items = line.strip()
        input_object.na_average_factor = items
        try:
            line = next_useful_line()
            items = line.strip()
            input_object.na_state = items
        except StopIteration:
            input_object.na_state = None
        file1.close()
        return input_object
    except StopIteration or IndexError:
        file1.close()
        return input_object


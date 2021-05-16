"""
run!!!
"""
import time
from abc import ABCMeta, abstractmethod
from copy import deepcopy
from math import sqrt, log, exp
from os import makedirs, path


class Element(object):
    def __init__(self):
        self.position = None
        self.measured_f = None
        self.operation_f = None
        self.designed_vacuum_f = None
        self.temperature = None
        self.humidity = None
        self.delta_f = None

    def vacuum_frequency(self):
        pass


class Measurement(metaclass=ABCMeta):
    """the parent class of measurements, need to rewrite run() in child"""

    def __init__(self):
        self.len_total = None
        self.len_step = None
        self.time_step = None
        self.num_of_measurements = None
        self.f0 = None
        self.temperature = None
        self.work_temperature = 24
        self.humidity = None
        self.access_sensor_times = None
        self.elements = []
        self.sensor = None
        self.motor = None
        self.network_analyzer = None
        self.f_r = None
        self.na_average_factor = 1
        self.multi_measure = 1

    def cal_cavity_frequency(self):
        """calculate real cavity resonance frequency according to design (vacuum) frequency"""

        if self.access_sensor_times >= 1:
            [self.temperature, self.humidity] = self.sensor.current_t_rh
        t_k = self.temperature + 273.15
        pw = vapor_pressure(t_k) * self.humidity
        pd = 760 - pw
        epsilon_r = 1 + 210e-6 * pd / t_k + 180e-6 * (1 + 3580 / t_k) * pw / t_k
        partial_f_partial_t = 48e3 * self.f0 / 2856e6
        delta_f = partial_f_partial_t * (self.temperature - self.work_temperature)
        self.f_r = (self.f0 + delta_f) / sqrt(epsilon_r)

    @abstractmethod
    def run(self):
        """need to rewrite in child class"""
        pass

    def measure_frequency(self):
        """if multi_measure > 2, return average f except for the maximum and minimum"""

        f_list = []
        for i in range(self.multi_measure):
            f_list.append(self.network_analyzer.resonance_frequency())
            time.sleep(0.1)
        if len(f_list) >= 3:
            ave_f = (sum(f_list) - max(f_list) - min(f_list)) / (self.multi_measure - 2)
        else:
            ave_f = sum(f_list) / self.multi_measure
        return ave_f

    def delta_f(self, measured_f):
        return self.f_r - measured_f

    def save_data(self, save_path):
        local_time = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
        file_path = save_path + '/' + local_time + '.txt'
        if not path.exists(save_path):
            makedirs(save_path)
        file = open(file_path, 'w')
        file.write('& 测量时间：' + local_time)
        file.write(str(self))
        file.write(self.network_analyzer.query_state())
        file.write('& 位置 频率 温度 湿度 Δf\n')
        for ele in self.elements:
            file.write(f'{ele.position:.2f} {ele.measured_f:.6e} {ele.temperature:.2f} '
                       f'{ele.humidity:.2f} {ele.delta_f:.6e}\n')
        file.close()

    def __str__(self):
        text = ''
        text += ('\n&    腔体长度 = ' + str(self.len_total) + ' mm')
        text += ("\n&    运动步长 = " + str(self.len_step) + ' mm')
        text += ("\n&    等待时间 = " + str(self.time_step) + ' s')
        text += ("\n&    真空频率 = " + str(self.f0 / 1e6) + 'MHz')
        text += ("\n&    温度 = " + str(self.temperature) + '℃')
        text += ("\n&    湿度 = " + str(self.humidity * 100) + '%')
        text += ("\n&    腔体频率 = " + str(self.f_r / 1e6) + 'MHz\n')
        return text


class LongitudinalMeasurement(Measurement):
    """measurement of longitudinal delta_f distribution"""

    def run(self):
        current_position = 0
        new_ele = Element()
        time.sleep(self.time_step)
        new_ele.position = current_position
        if self.access_sensor_times == 2:
            [self.temperature, self.humidity] = self.sensor.current_t_rh
        new_ele.temperature = self.temperature
        new_ele.humidity = self.humidity
        new_ele.measured_f = self.measure_frequency()
        new_ele.delta_f = self.delta_f(new_ele.measured_f)
        self.elements.append(deepcopy(new_ele))
        yield new_ele.position, new_ele.delta_f
        while abs(current_position) <= abs(self.len_total - self.len_step):
            self.motor.move_forward()
            current_position += self.len_step
            time.sleep(self.time_step)
            new_ele.position = current_position
            if self.access_sensor_times == 2:
                [self.temperature, self.humidity] = self.sensor.current_t_rh
            new_ele.temperature = self.temperature
            new_ele.humidity = self.humidity
            new_ele.measured_f = self.measure_frequency()
            new_ele.delta_f = self.delta_f(new_ele.measured_f)
            self.elements.append(deepcopy(new_ele))
            yield new_ele.position, new_ele.delta_f


class AngularMeasurement(Measurement):
    """angular"""

    def run(self):
        # todo: step
        angle_step = int(20000 / self.num_of_measurements)
        new_ele = Element()
        time.sleep(self.time_step)
        new_ele.measured_f = self.measure_frequency()
        new_ele.delta_f = self.delta_f(new_ele.measured_f)
        current_step = 0
        new_ele.position = current_step * 0.018
        if self.access_sensor_times == 2:
            [self.temperature, self.humidity] = self.sensor.current_t_rh
        new_ele.temperature = self.temperature
        new_ele.humidity = self.humidity
        self.elements.append(deepcopy(new_ele))
        yield new_ele.position, new_ele.delta_f
        while current_step < 20000:
            self.motor.move_forward()
            current_step += angle_step
            time.sleep(self.time_step)
            new_ele.measured_f = self.measure_frequency()
            new_ele.delta_f = self.delta_f(new_ele.measured_f)
            new_ele.position = current_step * 0.018
            if self.access_sensor_times == 2:
                [self.temperature, self.humidity] = self.sensor.current_t_rh
            new_ele.temperature = self.temperature
            new_ele.humidity = self.humidity
            self.elements.append(deepcopy(new_ele))
            yield new_ele.position, new_ele.delta_f


class Sensor(object):
    """temperature and humidity sensor, connect by USB comp

    the output of sensor is in ascii code, hex
    Example:
    54 3a 20 31 39 2e 39 35 2c 20 52 48 3a 20 30 2e 32 38 0d 0a
     T  :    1  9  .  9   5  ,    R  H  :     0  .  2  8  \r \n

     data[3: 8] is temperature, data[14: 18] is humidity
    """

    def __init__(self, ser):
        self.ser = ser

    @property
    def current_temperature(self):
        data = self.ser.readline().decode()
        try:
            temperature = float(data[3: 8])
            return temperature
        except Exception:
            raise Exception(f'cannot read temperature from data:\n    {data}')

    @property
    def current_humidity(self):
        data = self.ser.readline().decode()
        try:
            humidity = float(data[14: 18])
            return humidity
        except Exception:
            raise Exception(f'cannot read humidity from data:\n    {data}')

    @property
    def current_t_rh(self):
        """:return [t, rh]"""
        data = self.ser.readline().decode()
        try:
            temperature = float(data[3: 8])
            humidity = float(data[14: 18])
            return [temperature, humidity]
        except Exception:
            raise Exception(f'cannot read data:\n    {data}')

    def inspect_ser(self):
        try:
            data = self.ser.readline().decode()
            float(data[3: 8])
            float(data[14: 18])
        except Exception:
            raise Exception('sensor error, please check the serial port')

    def __str__(self):
        return self.ser.port


class StepMotor(object):
    """moons ST drive of step motor

    the command example:
        ser.write([0x31, 0x41, 0x43, 0x31, 0x30, 0x0D]) or ser.write(b'1AC10\r')
        0x31 is the address to write, don't change it!!!
        0x41 0x43 (AC) is the command to set or inquire acceleration
        0x31 0x30 (10) is the value of acceleration
        0x0D (\r) is the end of command, it's necessary!

    the step:
        the unit of motor moving is step, one step for 1.8 degree.
        in my experiment. THE DISTANCE CHANGES WITH THE RADIUS!!! 10000 steps is almost 36.33 mm.
    """

    def __init__(self, ser):
        self.ser = ser
        self.mm_for_10000_step = 36.33
        self.ser.write(b'1AC10\r')
        if self.ser.readline() != b'1%\r':
            raise Exception("step motor error: can't set acceleration")
        self.ser.write(b'1DE10\r')
        if self.ser.readline() != b'1%\r':
            raise Exception("step motor error: can't set DE")
        self.ser.write(b'1VE2\r')
        if self.ser.readline() != b'1%\r':
            raise Exception("step motor error: can't set VE")

    def move_forward(self, distance_mm=None, distance=None):
        if distance_mm is not None:
            step = int(distance_mm * 10000 / self.mm_for_10000_step)
        elif distance is not None:
            step = int(distance)
        else:
            step = ''
        command = '1FL' + str(step) + '\r'
        self.ser.write(command.encode())
        if self.ser.readline() != b'1%\r':
            raise Exception("step motor error: can't move")

    def set_distance(self, distance_mm=None, distance=None):
        if distance_mm is not None:
            step = int(distance_mm * 10000 / self.mm_for_10000_step)
        else:
            step = int(distance)
        command = '1DI' + str(step) + '\r'
        self.ser.write(command.encode())
        # print(self.ser.readline())
        if self.ser.readline() != b'1%\r':
            raise Exception("step motor error: can't set distance")


class NetworkAnalyzer(object):
    """Agilent E5071C

    the commands can be found on http://ena.support.keysight.com/e5071c/manuals/webhelp/eng/
    """

    def __init__(self, source, na_state=None, average_factor=None):
        self.na = source
        self.initial_setting(na_state, average_factor)

    def initial_setting(self, state, average_factor):
        if state is not None:
            self.na.write(f':MMEM:LOAD "{state}"')
        self.na.write(':DISP:WIND1:TRAC1:Y:AUTO')
        self.na.write(':CALC1:MARK1 ON')
        self.na.write(':CALC1:MARK1:FUNC:TYPE MIN')
        self.na.write(':CALC1:MARK1:FUNC:TRAC ON')
        if average_factor is None or average_factor == 1:
            self.na.write(':SENS1:AVER OFF')
        else:
            self.na.write(':SENS1:AVER ON')
            self.na.write(f':SENS1:AVER:COUN {average_factor:d}')
        data = self.na.query(':CALC1:MARK1:FUNC:TYPE?')
        time.sleep(0.3)
        if data != 'MIN\n':
            raise Exception('network analyzer communication error')

    def resonance_frequency(self):
        data = self.na.query_ascii_values(':CALC1:MARK1:DATA?')
        frequency = data[2]
        time.sleep(0.3)
        return frequency

    def query_state(self):
        center = self.na.query(':SENS1:FREQ:CENT?')
        span = self.na.query(':SENS1:FREQ:SPAN?')
        return f'& center = {center}& span = {span}'


def vapor_pressure(Kelven_temperature):
    """suitable for 0~50 Celsius

    DOI: 10. 13842/j.cnki.issn1671-8151.1996.03.020"""
    # todo: not so precise, maybe change to look-up table method
    lnp = 58.430772 - 6750.4344 / Kelven_temperature - 4.8668493 * log(Kelven_temperature)
    p = exp(lnp) / 133.322368
    return p

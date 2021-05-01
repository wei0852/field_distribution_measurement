"""
run!!!
"""
import random
import time
import os
import numpy as np
import copy
import serial


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


class Measurement(object):
    """the parent class of measurements, need to rewrite run() in child"""

    def __init__(self):
        self.len_total = None
        self.len_step = None
        self.time_step = None
        self.f0 = None
        self.f_r = None
        self.temperature = None
        self.work_temperature = 24
        self.work_f = 2856e6
        self.humidity = None
        self.access_sensor_times = None
        self.elements = []
        self.sensor = None
        self.motor = None
        self.network_analyzer = None

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
        self.f_r = (self.f0 + delta_f) / np.sqrt(epsilon_r)
        return self.f_r / 1e6

    def run(self):
        """need to rewrite in child class"""
        raise Exception(' ')

    def measure_frequency(self):
        return self.network_analyzer.resonance_frequency()

    def delta_f(self, measured_f):
        return self.f_r - measured_f

    def save_data(self, path):
        local_time = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
        file_path = path + '/' + local_time + '.txt'
        if not os.path.exists(path):
            os.makedirs(path)
        file = open(file_path, 'w')
        file.write('& 测量时间：' + local_time)
        file.write(str(self))
        file.write('& 位置 频率 真空频率 温度 湿度 归一化场强\n')
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
        new_ele.measured_f = self.measure_frequency()
        new_ele.delta_f = self.delta_f(new_ele.measured_f)
        new_ele.position = current_position
        if self.access_sensor_times == 2:
            [self.temperature, self.humidity] = self.sensor.current_t_rh
        new_ele.temperature = self.temperature
        new_ele.humidity = self.humidity
        self.elements.append(copy.deepcopy(new_ele))
        yield new_ele.position, new_ele.delta_f
        while abs(current_position) <= abs(self.len_total - self.len_step):
            self.motor.move_forward()
            current_position += self.len_step
            time.sleep(self.time_step)
            new_ele.measured_f = self.measure_frequency()
            new_ele.delta_f = self.delta_f(new_ele.measured_f)
            new_ele.position = current_position
            if self.access_sensor_times == 2:
                [self.temperature, self.humidity] = self.sensor.current_t_rh
            new_ele.temperature = self.temperature
            new_ele.humidity = self.humidity
            self.elements.append(copy.deepcopy(new_ele))
            yield new_ele.position, new_ele.delta_f


class TestMeasurement(Measurement):
    """only for test GUI, can't connect to step motor or network analysis"""

    def run(self):
        current_position = 0
        new_ele = Element()
        time.sleep(self.time_step)
        frequency = self.measure_frequency()
        normalized_field = self.delta_f(frequency)
        new_ele.position = current_position
        new_ele.measured_f = frequency
        new_ele.delta_f = normalized_field
        new_ele.temperature = self.temperature
        new_ele.humidity = self.humidity
        self.elements.append(copy.deepcopy(new_ele))
        yield new_ele.position, new_ele.delta_f
        while abs(current_position) <= abs(self.len_total - self.len_step):
            current_position += self.len_step
            time.sleep(self.time_step)
            frequency = self.measure_frequency()
            normalized_field = self.delta_f(frequency)
            new_ele.position = current_position
            new_ele.measured_f = frequency
            new_ele.delta_f = normalized_field
            new_ele.temperature = self.temperature
            new_ele.humidity = self.humidity
            self.elements.append(copy.deepcopy(new_ele))
            yield new_ele.position, new_ele.delta_f

    def measure_frequency(self):
        return self.f0 * random.random()


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
        assert isinstance(ser, serial.Serial)

    @property
    def current_temperature(self):
        data = self.ser.readline()
        temperature = float(data[3: 8])
        return temperature

    @property
    def current_humidity(self):
        data = self.ser.readline()
        humidity = float(data[14: 18])
        return humidity

    @property
    def current_t_rh(self):
        """:return [t, rh]"""
        data = self.ser.readline()
        temperature = float(data[3: 8])
        humidity = float(data[14: 18])
        return [temperature, humidity]

    def inspect_ser(self):
        try:
            data = self.ser.readline()
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
        the unit of motor moving is step, but I didn't find its definition. So I measured the distance for 10000 steps
        in my experiment. THE DISTANCE CHANGES WITH THE RADIUS!!!
        measurement results:
            36.5mm, 36.3mm, 36.2mm
        36.33mm for 10000 steps, that's enough, my experiment doesn't need too much accuracy of distance.
    """

    def __init__(self, ser, distance_mm=None):
        assert isinstance(ser, serial.Serial)
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
        if distance_mm is not None:
            step = int(distance_mm * 10000 / self.mm_for_10000_step)
            command = '1DI' + str(step) + '\r'
            self.ser.write(command.encode())
            if self.ser.readline() != b'1%\r':
                raise Exception("step motor error: can't set distance")

    def move_forward(self, distance_mm=None):
        if distance_mm is not None:
            step = int(distance_mm * 10000 / self.mm_for_10000_step)
        else:
            step = ''
        command = '1FL' + str(step) + '\r'
        self.ser.write(command.encode())
        if self.ser.readline() != b'1%\r':
            raise Exception("step motor error: can't move")

    def set_distance(self, distance_mm=None):
        if distance_mm is not None:
            step = int(distance_mm * 10000 / self.mm_for_10000_step)
        else:
            step = ''
        command = '1DI' + str(step) + '\r'
        self.ser.write(command.encode())
        if self.ser.readline() != b'1%\r':
            raise Exception("step motor error: can't set distance")


class NetworkAnalyzer(object):
    """Agilent E5071C

    the commands can be found on http://ena.support.keysight.com/e5071c/manuals/webhelp/eng/
    """

    def __init__(self, source):
        self.na = source
        self.initial_setting()

    def initial_setting(self):
        # self.na.write(':CALC1:TRAC1:FORM MLOG')  # set log mat format
        # self.na.write(':CALC1:PAR1:DEF S11')  # set measurement to S11
        self.na.write(':MMEM:LOAD "d:\ITC02-10MHZ2851.STA"')
        self.na.write(':CALC1:MARK1 ON')
        self.na.write(':CALC1:MARK1:FUNC:TYPE MIN')
        data = self.na.query(':CALC1:MARK1:FUNC:TYPE?')
        # set frequency range. center 2850MHz, span 0.50MHz
        # self.na.write(':SENS1:FREQ:CENT 2856000000')
        # self.na.write(':SENS1:FREQ:SPAN 50000000')
        # self.na.write(':DISP:WIND1:TRAC1:Y:AUTO')
        time.sleep(0.3)
        # fr = int(self.resonance_frequency())
        # self.na.write(':SENS1:FREQ:CENT ' + str(fr))
        # self.na.write(':SENS1:FREQ:SPAN 5000000')
        # self.na.write(':DISP:WIND1:TRAC1:Y:AUTO')
        if data != 'MIN\n':
            raise Exception('network analyzer communication error')

    def resonance_frequency(self):
        self.na.write(':CALC1:MARK1:FUNC:EXEC')
        data = self.na.query_ascii_values(':CALC1:MARK1:DATA?')
        frequency = data[2]
        time.sleep(0.2)
        return frequency


def vapor_pressure(Kelven_temperature):
    """suitable for 0~50 Celsius

    DOI: 10. 13842/j.cnki.issn1671-8151.1996.03.020"""
    # todo: not so precise, maybe change to look-up table method
    lnp = 58.430772 - 6750.4344 / Kelven_temperature - 4.8668493 * np.log(Kelven_temperature)
    p = np.exp(lnp) / 133.322368
    return p

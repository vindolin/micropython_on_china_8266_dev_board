import machine as m
import dht as _dht
from networks import networks
from wifi import connect
import time

pin_dht = m.Pin(4)
pin_buzzer = m.Pin(5, m.Pin.OUT)
pin_relais = m.Pin(16, m.Pin.OUT)

pin_white_led = m.PWM(m.Pin(14), freq=1000)

pins_rgb = {
    'r': m.PWM(m.Pin(15), freq=1000),
    'g': m.PWM(m.Pin(13), freq=1000),
    'b': m.PWM(m.Pin(12), freq=1000),
}

pin_button_s2 = m.Pin(0, m.Pin.IN, m.Pin.PULL_UP)
pin_button_s3 = m.Pin(2, m.Pin.IN, m.Pin.PULL_UP)

pin_adc = m.ADC(0)

r = m.reset

wifi = connect(networks)

# dht = _dht.DHT11(pin_dht)  # if you have a blue module
dht = _dht.DHT22(pin_dht)  # if you have a white module


def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def measure():
    dht.measure()
    print('Temperature: {}\nHumidity: {}'.format(dht.temperature(), dht.humidity()))


def buzzer(value):
    pin_buzzer.value(value)


def relais(value):
    pin_relais.value(value)


def rgb(r, g, b):
    pins_rgb['r'].duty(r)
    pins_rgb['g'].duty(g)
    pins_rgb['b'].duty(b)


def led_white(value):
    pin_white_led.duty(value)


def button_s2():
    return not pin_button_s2.value()


def button_s3():
    return not pin_button_s3.value()


def adc_loop():
    while True:
        value = pin_adc.read()
        value = int(map_value(value, 0, 1024, 0, 1000))
        print(value)
        led_white(value)
        time.sleep(0.02)

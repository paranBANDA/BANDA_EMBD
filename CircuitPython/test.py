import machine

sda = machine.Pin(0)
scl = machine.Pin(1)

i2c = machine.I2C(0, sda=sda, scl=scl, freq=400000)

print('I2C address: ')
print(hex(i2c.scan()[0]))

import bitbangio
from board import *

i2c = bitbangio.I2C(SCL, SDA)
print(i2c.scan())
i2c.deinit()
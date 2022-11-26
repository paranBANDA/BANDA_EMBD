from imu import MPU6050  # https://github.com/micropython-IMU/micropython-mpu9x50
import time
from machine import Pin, I2C, UART

i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=400000)
imu = MPU6050(i2c)

uart = UART(0, 9600)

t_ax=0
t_ay=0
t_az=0
t_gx=0
t_gy=0
t_gz=0

def ble(a_x, a_y, a_z, g_x, g_y, g_z):
    command = uart.read()
    if command == b'1':
        print("Acceleration x: ", a_x, " y:", a_y, "z: ", a_z)
        print("gyrometre x: ", g_x, " y:", g_y, "z: ", g_z)
        uart.write('a_x: '+str(a_x)+', a_y: '+str(a_y)+', a_z: '+str(a_z))
        uart.write('g_x: '+str(g_x)+', g_y: '+str(g_y)+', a_z: '+str(g_z))
            
#connect bluetooth
while True:
    if uart.any():
        break

while True:
    acceleration = imu.accel
    gyrometre = imu.gyro
    
    a_x = round(acceleration.x,2)
    a_y = round(acceleration.y,2)
    a_z = round(acceleration.z,2)
    g_x = round(gyrometre.x,2)
    g_y = round(gyrometre.y,2)
    g_z = round(gyrometre.z,2)
    
    ble(a_x, a_y, a_z, g_x, g_y, g_z)
    
    '''
    if a_x > t_ax and a_y > t_ay and a_z > t_az:
        if g_x > t_gx and g_y > t_gy and g_z > t_gz:
            ble(a_x, a_y, a_z, g_x, g_y, g_z)
    '''
    time.sleep(1)

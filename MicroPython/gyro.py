from imu import MPU6050  # https://github.com/micropython-IMU/micropython-mpu9x50
import time
from machine import Pin, I2C

now = time

i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=400000)
imu = MPU6050(i2c)

# Affichage de la température
print("Temperature: ", round(imu.temperature,2), "°C")

while True:
    # lecture des valeurs
    acceleration = imu.accel
    gyrometre = imu.gyro
    
    print (now.localtime())
    print ("Acceleration x: ", round(acceleration.x,2), " y:", round(acceleration.y,2),
           "z: ", round(acceleration.z,2))

    print ("gyrometre x: ", round(gyrometre.x,2), " y:", round(gyrometre.y,2),
           "z: ", round(gyrometre.z,2))
    
    time.sleep(1)
# interprétation des données (accéléromètre)
'''
    if abs(acceleration.x) > 0.8:
        if (acceleration.x > 0):
            print("x축이 위로 향합니다.")
        else:
            print("x축이 아래로 향합니다.")

    if abs(acceleration.y) > 0.8:
        if (acceleration.y > 0):
            print("y축이 위로 향합니다.")
        else:
            print("y축이 아래로 향합니다.")

    if abs(acceleration.z) > 0.8:
        if (acceleration.z > 0):
            print("z축이 위로 향합니다.")
        else:
            print("z축이 아래로 향합니다.")
'''
# interprétation des données (gyrometre)
'''
    if abs(gyrometre.x) > 20:
        print("x축 주위를 회전")

    if abs(gyrometre.y) > 20:
        print("y축 주위를 회전")

    if abs(gyrometre.z) > 20:
        print("z축 주위를 회전")
  
    time.sleep(0.2)
'''

import smbus			#import SMBus module of I2C
from time import sleep          #import
import picamera
import time
import requests
import info
import json

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value

idx = 0
def capture_img():
    global idx
    print("Capture image!")
    camera.capture('snapshot'+str(idx)+'.jpg')
    send_img()
    idx += 1

def send_img():
    f = open('snapshot'+str(idx)+'.jpg', 'rb')
    print("send image - snapshot"+str(idx)+".jpg")
    #requests.post('http://13.124.202.212:3000/polaroid/uploaddiaryimage', files={'files':f}, data=json.dumps(info.info))
    f.close()

# Main
bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init()

# camera init
camera = picamera.PiCamera()
camera.resolution = (2592, 1944) # (64, 64) ~ (2592, 1944) px

# main logic
zeroAx, zeroAy, zeroAz, zeroGx, zeroGy, zeroGz = 0, 0, 0, 0, 0, 0
def zeroing(n):
	sumAx, sumAy, sumAz, sumGx, sumGy, sumGz = 0, 0, 0, 0, 0, 0
	global zeroAx, zeroAy, zeroAz, zeroGx, zeroGy, zeroGz
	for i in range(n):
		sumAx += read_raw_data(ACCEL_XOUT_H) / 16384.0
		sumAy += read_raw_data(ACCEL_YOUT_H) / 16384.0
		sumAz += read_raw_data(ACCEL_ZOUT_H) / 16384.0
		sumGx += read_raw_data(GYRO_XOUT_H) / 131.0
		sumGy += read_raw_data(GYRO_YOUT_H) / 131.0
		sumGz += read_raw_data(GYRO_ZOUT_H) / 131.0
		sleep(0.05)		
	zeroAx = sumAx / n
	zeroAy = sumAy / n
	zeroAz = sumAz / n
	zeroGx = sumGx / n
	zeroGy = sumGy / n
	zeroGz = sumGz / n

zeroing(10)
print(zeroAx, zeroAy, zeroAz, zeroGx, zeroGy, zeroGz)
height, leftright = 0, 0
print (" Reading Data of Gyroscope and Accelerometer")

sumAx, sumAy, sumAz, sumGx, sumGy, sumGz = 0, 0, 0, 0, 0, 0
prevStatus = 0
while True:
	print("Start sensing")
	in_data = int(input())
	if in_data == 0:
		arr=[]
		sum=0
		for i in range(10):
			sumAx += read_raw_data(ACCEL_XOUT_H) / 16384.0
			sumAy += read_raw_data(ACCEL_YOUT_H) / 16384.0
			sumAz += read_raw_data(ACCEL_ZOUT_H) / 16384.0
			sumGx += read_raw_data(GYRO_XOUT_H) / 131.0
			sumGy += read_raw_data(GYRO_YOUT_H) / 131.0
			sumGz += read_raw_data(GYRO_ZOUT_H) / 131.0
			sleep(0.05)
		aveAx = sumAx / 10
		aveAy = sumAy / 10
		aveAz = sumAz / 10
		aveGx = sumGx / 10
		aveGy = sumGy / 10
		aveGz = sumGz / 10

		# diff height max = 1 / min = -1
		# 5: 0.6~1, 4: 0.2~0.6, 3: -0.2~0.2, 2: -0.6~-0.2, 1: -1~-0.6
		diffAx = aveAx - zeroAx
		if diffAx > 0.6:
			height = 5
		elif diffAx > 0.2:
			height = 4
		elif diffAx > -0.2:
			height = 3
		elif diffAx > -0.6:
			height = 2
		elif diffAx > -1:
			height = 1
		
		# horz left = -1 . right = 1
		if aveAy > 0.6:
			leftright = 5
		elif aveAy > 0.2:
			leftright = 4
		elif aveAy > -0.2:
			leftright = 3
		elif aveAy > -0.6:
			leftright = 2
		elif aveAy > -1:
			leftright = 1

		print("height:", height)
		print("leftright:", leftright)
		
		cnt = 0
		for i in range(30):
			acc_x = read_raw_data(ACCEL_XOUT_H)
			acc_y = read_raw_data(ACCEL_YOUT_H)
			acc_z = read_raw_data(ACCEL_ZOUT_H)
			gyro_x = read_raw_data(GYRO_XOUT_H)
			gyro_y = read_raw_data(GYRO_YOUT_H)
			gyro_z = read_raw_data(GYRO_ZOUT_H)
			Ax = acc_x/16384.0
			Ay = acc_y/16384.0
			Az = acc_z/16384.0
			Gx = gyro_x/131.0
			Gy = gyro_y/131.0
			Gz = gyro_z/131.0
			F = (abs(Ax) + abs(Ay) + abs(Az))/3.00
			print ("F=%.2f" %F)
			if F < 0.35:
				continue
			sum += F
			cnt += 1 #error exception
			sleep(0.05)
			# print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az)

		try:
			avg=sum / cnt
		except:
			continue
	
		force = 0
		if avg > 1.4:
			force = 5
		elif avg > 1.1:
			force = 4
		elif avg > 0.8:
			force = 3
		elif avg > 0.6:
			force = 2
		elif avg > 0.4:
			force = 1
		
		print("force:",avg)		# min = 0.5 max = 2
		# leftright calc again


		# 1: 분노, 2: 공포, 3: 복종, 4: 경계, 5: 놀람, 6: 편안, 7: 자신감, 8: 행복
		status = 0
		if height == 5:
			if force == 2 or force == 3:
				status = 5				# 놀람
			if leftright == 1 or leftright == 2:
				if force == 0 or force == 1:
					status = 4			# 경계
				if force == 2 or force == 3:
					status = 1			# 분노
		if height == 2 or height == 3 or height == 4:
			if height == 4:
				if leftright == 3:
					if force == 0 or force == 1:
						status = 7		# 자신감
			else:
				if leftright == 4 or leftright == 5:
					if force == 2 or force == 3:
						status = 6		# 편안
					if force == 4 or force == 5:
						status = 8		# 행복
		if height == 1:
			if leftright == 1 or leftright == 2:
				if force == 0 or force == 1:
					status = 2			# 공포
				if force == 2 or force == 3:
					status = 3			# 복종

		print("status:",status)
		if status != prevStatus and status != 0 and status != 6:
			capture_img()
		prevStatus = status

	print("Sleep")
	sleep(1)

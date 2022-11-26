import picamera
import time

camera = picamera.PiCamera()
camera.resolution = (2592, 1944) # (64, 64) ~ (2592, 1944) px

idx = 0
for i in range(10):
	time.sleep(2)
	camera.capture('snapshot'+str(i)+'.jpg')
	idx += 1

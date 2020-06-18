import time
from datetime import datetime as dt
import FaBo9Axis_MPU9250
from bmp280 import BMP280
from smbus2 import SMBus
from picamera import PiCamera
import threading

# Initialise the MPU9250 (accelerometer and gyroscope)
mpu9250 = FaBo9Axis_MPU9250.MPU9250()

# Initialise the BMP280 (temperature and pressure)
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)

# Initialise some more variables
dt_str = dt.now().strftime("%Y-%m-%dT%H:%M:%S")
data_file = f"data/flight_{dt_str}.txt"
video_file = f"videos/flight_{dt_str}.h264"
interval = 0.5 # secs
fd_file = open(data_file, "a") # Append mode
fd_file.write(f"Flight data starting from {dt_str}, in intervals of {interval}s\n\n---\n\n")
camera = PiCamera()
camera.resolution = (640, 480)

def record_video(camera, fd_filename):
    camera.start_recording(video_file)
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        camera.stop_recording()
thr = threading.Thread(target = record_video, args=[camera, fd_filename])
thr.daemon = True
thr.start()

while True:
    accel = mpu9250.readAccel()
    gyro = mpu9250.readGyro()
    mag = mpu9250.readMagnet()
    temperature = bmp280.get_temperature()
    pressure = bmp280.get_pressure()

    fd_file = open(data_file, "a")
    fd_file.write(f"Acceleration: {accel['x']}, {accel['y']}, {accel['z']}\n")
    fd_file.write(f"Gyroscope: {gyro['x']}, {gyro['y']}, {gyro['z']}\n")
    fd_file.write(f"Magnet: {mag['x']}, {mag['y']}, {mag['z']}\n")
    fd_file.write("Temperature: " + "{:.3f}".format(temperature) + "C\n")
    fd_file.write("Pressure: " + "{:.3f}".format(pressure) + "hPa\n")
    fd_file.write("\n")
    fd_file.close()

    time.sleep(interval)


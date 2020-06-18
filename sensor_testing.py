import time
import FaBo9Axis_MPU9250
from bmp280 import BMP280
from smbus2 import SMBus

# Initialise the MPU9250 (accelerometer and gyroscope)
mpu9250 = FaBo9Axis_MPU9250.MPU9250()

# Initialise the BMP280 (temperature and pressure)
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)

while True:
    accel = mpu9250.readAccel()
    gyro = mpu9250.readGyro()
    mag = mpu9250.readMagnet()
    temperature = bmp280.get_temperature()
    pressure = bmp280.get_pressure()

    print (f"Acceleration: {accel['x']}, {accel['y']}, {accel['z']}")
    print (f"Gyroscope: {gyro['x']}, {gyro['y']}, {gyro['z']}")
    print (f"Magnet: {mag['x']}, {mag['y']}, {mag['z']}")
    print ("Temperature: " + "{:.3f}".format(temperature) + "C")
    print ("Pressure: " + "{:.3f}".format(pressure) + "hPa")
    print ()

    time.sleep(1)

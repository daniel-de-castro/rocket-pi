import time
import FaBo9Axis_MPU9250
from bmp280 import BMP280
from smbus2 import SMBus

# Initialise the MPU9250 (accelerometer, gyroscope and magnetometer)
mpu9250 = FaBo9Axis_MPU9250.MPU9250()

# Initialise the BMP280 on bus 1 (temperature and pressure)
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)

isRunning = True
while isRunning:
    accelerometer = mpu9250.readAccel()
    gyroscope = mpu9250.readGyro()
    magnetometer = mpu9250.readMagnet()
    temperature = bmp280.get_temperature()
    pressure = bmp280.get_pressure()

    print(f"Acceleration: {accelerometer['x']}, {accelerometer['y']}, {accelerometer['z']}")
    print(f"Gyroscope: {gyroscope['x']}, {gyroscope['y']}, {gyroscope['z']}")
    print(f"Magnet: {magnetometer['x']}, {magnetometer['y']}, {magnetometer['z']}")
    print("Temperature: " + "{:.3f}".format(temperature) + " C")
    print("Pressure: " + "{:.3f}".format(pressure) + " hPa")
    print()

    # Break the loop if we want to stop executing.
    if not isRunning:
        break

    time.sleep(1)

import asyncio
import time
import datetime
import random
import websockets
import FaBo9Axis_MPU9250
from bmp280 import BMP280
from smbus2 import SMBus

# Initialise the MPU9250 (accelerometer and gyroscope)
mpu9250 = FaBo9Axis_MPU9250.MPU9250()

# Initialise the BMP280 (temperature and pressure)
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)

async def time(websocket, path):
    while True:
        timestamp = datetime.datetime.utcnow().strftime("%H:%M:%S")
        accel = mpu9250.readAccel()
        gyro = mpu9250.readGyro()
        mag = mpu9250.readMagnet()
        temperature = bmp280.get_temperature()
        pressure = bmp280.get_pressure()

        await websocket.send('|'.join([ timestamp, "{:.3f}".format(temperature), "{:.3f}".format(pressure) ]))
        await asyncio.sleep(1)

start_server = websockets.serve(time, "192.168.0.8", 8001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

#print (f"Acceleration: {accel['x']}, {accel['y']}, {accel['z']}")
#print (f"Gyroscope: {gyro['x']}, {gyro['y']}, {gyro['z']}")
#print (f"Magnet: {mag['x']}, {mag['y']}, {mag['z']}")
#print ("Temperature: " + "{:.3f}".format(temperature) + "C")
#print ("Pressure: " + "{:.3f}".format(pressure) + "hPa")

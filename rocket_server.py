import asyncio
import time
import datetime
import random
import websockets
import FaBo9Axis_MPU9250
from bmp280 import BMP280
from smbus2 import SMBus

# Initialise the BMP280 (temperature, pressure and altitude)
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)

pressure_vals = []
for i in range(5):
    pressure_vals.append(bmp280.get_pressure())
    time.sleep(0.5)

pressure_base = sum(pressure_vals) / len(pressure_vals)

# Initialise the MPU9250 (accelerometer and gyroscope)
mpu9250 = FaBo9Axis_MPU9250.MPU9250()

async def time(websocket, path):
    while True:
        timestamp = datetime.datetime.utcnow().strftime("%H:%M:%S")
        altitude = bmp280.get_altitude(qnh=pressure_base)
        temperature = bmp280.get_temperature()
        pressure = bmp280.get_pressure()
        accel = mpu9250.readAccel()
        gyro = mpu9250.readGyro()
        mag = mpu9250.readMagnet()

        await websocket.send('|'.join([ timestamp, "{:.2f}".format(altitude), "{:.3f}".format(temperature), "{:.3f}".format(pressure), f"{accel['x']},{accel['y']},{accel['z']}", f"{gyro['x']},{gyro['y']},{gyro['z']}", f"{mag['x']},{mag['y']},{mag['z']}" ]))
        await asyncio.sleep(1)

start_server = websockets.serve(time, "192.168.0.8", 8001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

#print (f"Acceleration: {accel['x']}, {accel['y']}, {accel['z']}")
#print (f"Gyroscope: {gyro['x']}, {gyro['y']}, {gyro['z']}")
#print (f"Magnet: {mag['x']}, {mag['y']}, {mag['z']}")
#print ("Temperature: " + "{:.3f}".format(temperature) + "C")
#print ("Pressure: " + "{:.3f}".format(pressure) + "hPa")

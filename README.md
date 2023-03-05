# RocketPi

<img width="630" alt="image" src="https://user-images.githubusercontent.com/32271509/197417106-b628fc98-9a75-4449-bd2a-07572e2f73e1.png">

## Table of Contents

- [Overview](#overview)
- [BOM](#bom)
- [Set up the Raspberry Pi](#set-up-the-raspberry-pi)
  - [Configure the OS](#configure-the-os)
  - [Set up the sensors](#set-up-the-sensors)
- [Set up a debugging environment](#set-up-a-debugging-environment)
  - [SSH into the Raspberry Pi](#ssh-into-the-raspberry-pi)
  - [Python Development](#python-development)
    - [I2C](#i2c)
    - [BMP-280](#bmp-280)
    - [RPi Cam Interface](#rpi-cam-interface)

## Overview

- **flight_data_logger.py**: reads rocket flight data and logs it to a file.
- **rocket_server.py**: reads rocket flight data and broadcasts it.
- **sensor_tester.py**: used to check whether the sensors are working.

## BOM

| Component | Description | Source | Price |
|:---------:|:-----------:|:------:|:-----:|
| Raspberry Pi Zero W | Version 1.3 | [Pimoroni](https://shop.pimoroni.com/products/raspberry-pi-zero-w) | £9.30 |
| MicroSD Card | 64GB | [Amazon](https://www.amazon.co.uk/SanDisk-microSDXC-Memory-Adapter-Performance/dp/B073JYVKNX/ref=sr_1_2) | £17.49 |
| Camera | Camera for Raspberry Pi Zero | [Pimoroni](https://shop.pimoroni.com/products/raspberry-pi-zero-camera-module) | £14.10 |
| LiPo SHIM | Enables the RPi to be power supplied from a battery | [Pimoroni](https://shop.pimoroni.com/products/lipo-shim) | £12.60 |
| LiPo Battery | 150mAh | [Pimoroni](https://shop.pimoroni.com/products/lipo-battery-pack) | £5.10 |
| GY-91 | A chip combining an MPU-9250 and a BMP280 | [ebay](https://www.ebay.co.uk/itm/273021805739) | £14.95 |


## Set up the Raspberry Pi

Before we can start programming, we need to setup the Raspberry Pi we will be using.

### Configure the OS

- On an SD card, flash the latest version of Raspberry Pi OS using [Raspberry Pi Imager](https://www.raspberrypi.com/software/).
- Setup WPA on the Imager application or through adding a `wpa_supplicant.conf` file in the SD card:
```
country=gb
update_config=1
ctrl_interface=/var/run/wpa_supplicant
network={
 scan_ssid=1
 ssid="MyNetworkSSID"
 psk="MyNetworkPassword"
}
```
- Setup a user for the Raspberry Pi through the Imager with a username and password.
- Setup SSH by adding an empty file called `ssh` in the SD card.

After the SD card has been flashed, we can insert it into our Raspberry Pi and power it up. When booting, the Raspberry Pi consumes the `wpa_supplicant.conf` and `ssh` files.

### Set up the sensors

To gather flight data, we are using the GY-91 module, which combines an MPU-9250 (accelerometer, gyroscope and magnetometer) and a BMP280 (temperature and pressure sensor).

The Raspberry Pi in the diagram below is different from the Raspberry Pi Zero W we are using, but the wiring configuration to connect the GY-91 should be the same.

<img width="1402" alt="image" src="https://user-images.githubusercontent.com/32271509/197072073-bcc5228b-2ce2-406d-a35d-7ada644a868c.png">

## Set up a debugging environment

### SSH into the Raspberry Pi

With the Raspberry Pi now booted up, we can scan our network with an application such as [MobaXterm](https://mobaxterm.mobatek.net/) to find the IP address with which we can start an SSH session.
The Raspberry Pi will prompt us to log in with a username and password, which should be the ones we set when configuring it.

### Python Development

Python already comes installed with the OS.

#### I2C

In order to read from the I2C from Python, we need to install the smbus module
```
sudo apt-get install python-smbus
```

You can run the following command to scan an I2C bus for devices. It outputs a table with the list of detected devices on the specified bus.
```
i2cdetect -y 1
```

#### BMP-280

This library is needed so that Python can read from the BMP280 sensor
```
sudo apt-get install build-essential python-pip python-dev python-smbus git
git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
cd Adafruit_Python_GPIO
sudo python setup.py install
```

#### RPi Cam Interface

RPi Cam Web Interface is a web interface for the Raspberry Pi Camera module. It can be used for a wide variety of applications including surveillance, DVR recording and time lapse photography. We will be using it to capture images and live video from the camera. 

Connect the camera with the Raspberry Pi Zero W and proceed with the instructions below.

```
git clone https://github.com/silvanmelchior/RPi_Cam_Web_Interface.git
cd RPi_Cam_Web_Interface
./install.sh
```

## Sample flight recording

https://user-images.githubusercontent.com/32271509/222975885-8085ed1b-c0ab-44f2-badf-97094f7ed585.mp4


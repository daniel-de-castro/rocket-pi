# RocketPi

## Overview

- **flight_data_logger.py**: reads rocket flight data and logs it to a file.
- **rocket_server.py**: reads rocket flight data and broadcasts it.
- **sensor_tester.py**: used to check whether the sensors are working.

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

## SSH into the Raspberry Pi

With the Raspberry Pi now booted up, we can scan our network with an application such as [MobaXterm](https://mobaxterm.mobatek.net/) to find the IP address with which we can start an SSH session.
The Raspberry Pi will prompt us to log in with a username and password, which should be the ones we set when configuring it.

## Set up a debugging environment

Python already comes installed with the OS.

TODO talk about the libraries to be imported (refer to other repo)

TODO i2cdetect -y 1

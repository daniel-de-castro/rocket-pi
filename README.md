# RocketPi

- record_flight_data.py - reads rocket flight data every 0.5 second and appends it to a txt file
- rocket_server.py - reads rocket flight data and broadcasts it.py
- sensor_testing.py - used to check whether the sensors are working

# Set up the Raspberry Pi

## Configure the OS

- On an SD card, flash the latest version of RaspberryPi OS using [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
- Setup WPA on the Imager application or through adding a `wpa_supplicant.conf` file in the SD card:
country=gb
update_config=1
ctrl_interface=/var/run/wpa_supplicant
network={
 scan_ssid=1
 ssid="MyNetworkSSID"
 psk="MyNetworkPassword"
}
- Setup a user for the Raspberry Pi through the Imager with a username and password
- Setup SSH by adding an empty file called `ssh` in the SD card

When booting, the Raspberry Pi consumes the `wpa_supplicant.conf` and `ssh` files.

## Set up the sensors

TODO talk about the sensors being used

TODO show how to connect the sensors to the Pi using the wires

# SSH into the Raspberry Pi

After booting up the Pi, you can scan your network with an application such as [MobaXterm](https://mobaxterm.mobatek.net/) to find the IP address with which you can start an SSH session.
The Pi will prompt you to log in with a username and password, which should be the ones you set when configuring it.

# Set up a debugging environment

Python already comes installed with the OS.

TODO talk about the libraries to be imported (refer to other repo)

TODO i2cdetect -y 1

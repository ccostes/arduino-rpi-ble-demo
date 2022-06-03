# Arduino RP2040 / Raspberry Pi BLE Demo
The project demonstrates a Raspberry Pi acting as a Bluetooth Low Energy (BLE) Peripheral that allows reading/writing a single data value, and an Arduino client which periodically connects and writes data.

# Installation
## Raspberry Pi
Install the `dbus` library via 
```
sudo apt install build-essential libdbus-glib-1-dev libgirepository1.0-dev
pip install dbus-python
```

## Arduino
Install the ArduinoBLE package.

# Ardunio Configuration
The Arduino scans for a specific device address which you'll need to get from the Pi with the command `echo -e 'show\nquit' | sudo bluetoothctl` which should produce output that looks like:
```
Controller XX:XX:XX:XX:XX:XX (public)
	Name: raspberrypi
	Alias: LighthouseWeatherStation
	...
```
The string that looks like `XX:XX:XX:XX:XX:XX` is what you want - copy that and paste it into the `#define PERIPHERAL_ADDR "XX:XX:XX:XX:XX:XX"` line in the arduino code.

# Running
Start the service on the Pi via `sudo python3 main.py` which should output:
```
GATT application running
GATT application registered
GATT advertisement registered
```

When the Arduino is running you should see lines like `Value received: 309` every second as the Ardunio sends data to the Pi via BLE!

# Credits
The Raspberry Pi portion of this project is basically a stripped down version of this [Lighthouse Weather Station](https://github.com/gitdefllo/lighthouse-weather-station) project.
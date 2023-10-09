# gamepademu
GamePad Emulator for iOS Guitar Hero Guitar

This is a Gamepad Emulator Where you can use your iOS Guitar Hero 6 fret Guitar in any game incluying Clone Hero.
Using a Raspberry PI Zero W use a BLE to connect to the guitar and emulate via USB a GamePad on the Computer. 
Windows / Linux / Mac.

## Requirements

A Raspberry PI Zero W, 
,Micro USB Data Cable
,SD Card Minimun 8GB.


## Installation

Please follow all the instructions to install Raspbian Bullseye Lite Image into a Raspberry PI Zero W also you need to get
Enable Wifi Connection and SSH access to this PI to perform this installation.


```bash
wget -O - https://raw.githubusercontent.com/josephillips85/gamepademu/master/installer/install.sh | sudo bash
```
## Usage

After follow the installation the Raspberry PI is ready to Emulate the Guitar.
Please Connect the Micro USB Cable on port USB (not PWR) on the Rasperry Pi Side
and in the computer .. You are ready to Rock....

![Where to connect USB Cable](https://github.com/josephillips85/gamepademu/raw/master/piconnect1.png)

Wait until the PI Boot

The Raspberry PI LED show the state of the driver.
Blinking each 3 Seconds Means the driver is looking for the guitar.
Steady Green Means Guitar is Connected.

## Donations

Who want to donate to this project. please doit via Paypal to
https://www.paypal.com/paypalme2/josephillips85

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
Copyright 2023 Jose Phillips
GNU General Public License v3.0 See License

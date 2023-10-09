#!/bin/bash


if [ -e /etc/os-release ]; then
    . /etc/os-release

    if [ "$PRETTY_NAME" = "Raspbian GNU/Linux 11 (bullseye)" ]; then
        echo "Installing Gamepad Emulator for iOS Guitar for Raspbian Bullseye"

        echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt   
        echo "dwc2" | sudo tee -a /etc/modules
        echo "libcomposite" | sudo tee -a /etc/modules
        apt -y update
        apt install -y python3-pip
        yes | pip install pygatt
        yes | pip install pexpect
        apt install -y git 

        mkdir -p /opt/gamepademu
        git clone https://github.com/josephillips85/gamepademu.git /tmp/gamepademu
        cp -r /tmp/gamepademu/Core/*  /opt/gamepademu
        chmod +x /opt/gamepademu/iosghsubsys.py

        cp /opt/gamepademu/gamepademu.service /lib/systemd/system/
        chmod 644 /lib/systemd/system/gamepademu.service
        systemctl daemon-reload
        systemctl enable gamepademu.service

        #Avoiding conflict dependency bluetooth an deprecated GATTTOOLS
        systemctl stop bluetooth
        systemctl disable bluetooth

        echo "Please restart your Rasbperry pi to changes take effect."
        echo "If you like this software please donate https://paypal.me/josephillips85?locale.x=en_US"

        
    elif [ "$PRETTY_NAME" = "Raspbian GNU/Linux 10 (buster)" ]; then
        echo "Raspbian Buster detected. Performing Unsupported instalastion on Buster"

        echo "Installing Gamepad Emulator for iOS Guitar"

        echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
        echo "dwc2" | sudo tee -a /etc/modules
        echo "libcomposite" | sudo tee -a /etc/modules

        apt -y update
        apt install -y python-pip
        yes | pip install pygatt
        yes | pip install pexpect
        apt install -y git 
        mkdir -p /opt/gamepademu

        #Requiered Clone from my repository because pygatt is still not patched.
        git clone https://github.com/josephillips85/pygatt.git /tmp/pygatt -b v1.1
        git clone https://github.com/josephillips85/gamepademu.git /tmp/gamepademu -b v1.1

        cp -r /tmp/pygatt/pygatt /opt/gamepademu
        cp -r /tmp/gamepademu/Core/*  /opt/gamepademu
        chmod +x /opt/gamepademu/iosghsubsys.py

        cp /opt/gamepademu/gamepademu.service /lib/systemd/system/
        chmod 644 /lib/systemd/system/gamepademu.service
        systemctl daemon-reload
        systemctl enable gamepademu.service

        echo "Please restart your Rasbperry pi to changes take effect."
        echo "If you like this software please donate https://paypal.me/josephillips85?locale.x=en_US"


    else
        echo "Raspberry Pi OS version not recognized. Stopping."
        exit 1
    fi
else
    echo "/etc/os-release not found. Stopping."
    exit 1
fi
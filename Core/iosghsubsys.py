#! /usr/bin/python
import subprocess 
import time
import sys
import pygatt.backends
import hidgamepad
from binascii import hexlify
Debug = False
Controller = ""
adapter = pygatt.backends.GATTToolBackend(search_window_size=2048)
if len(sys.argv) >= 2 and str(sys.argv[1]) == "-d":
    Debug = True


def setupPI():
     #Stop BT service to allow GATTools take control
     stop_bt = ["systemctl","stop","bluetooth"]
     subprocess.run (stop_bt ,check=True)
     with open("/sys/class/leds/ACT/trigger", "w") as f:
        f.write('none\n')
    

def blinkled():
    time.sleep(1)
    with open("/sys/class/leds/ACT/brightness", "w") as f:
        f.write('0\n')
    time.sleep(1)
    with open("/sys/class/leds/ACT/brightness", "w") as f:
        f.write('1\n')


def searchguitar():
    print ("Searching for iOS GH Live Guitar Controller")
    Controller = ""
    while Controller == "":
        blinkled()
        ghcontroller = discovery()
        if ghcontroller is not None:
            Controller = ghcontroller
            print ("Controller Found")
            print ("Connecting to controller at address: " + ghcontroller)
            connect(ghcontroller)


def handle_data(handle, value):
    # Get Data from subscription.
    if Debug:
        print ("Received data:" + str(hexlify(value)))
    # Send Raw Message to process
    hidgamepad.process(value)


def discovery():
    adapter.reset()
    list = adapter.scan(timeout=2)
    for x in list:
        if x["name"] == "Ble Guitar":
            return x["address"]


def disconnected(handle):
    adapter.stop()
    print ("Controller has been disconnected.")
    searchguitar()


def connect(address):
    try:
        adapter.start()
        ADDRESS_TYPE = pygatt.BLEAddressType.random
        device = adapter.connect(address, address_type=ADDRESS_TYPE)
        # Perform Subscribe on non standard way.
        device.char_write_handle(16, bytearray([0x1]))
        # Subscribe to characteristic
        device.subscribe("533e1524-3abe-f33f-cd00-594e8b0a8ea3",
                         callback=handle_data, wait_for_response=False)
        device.register_disconnect_callback(callback=disconnected)
        # Led Stay On
        with open("/sys/class/leds/ACT/brightness", "w") as f:
            f.write('100\n')
        print ("Guitar Connected.")
        # Keep the execution.
        #x = input("")
        while True:
            time.sleep(0.01)
    finally:
        adapter.stop()


print ("Gamepad Emulator v1.2 for iOS GH Live Guitar")
print ("--------------------------------------------")
print ("")

setupPI()
hidgamepad.init()
searchguitar()
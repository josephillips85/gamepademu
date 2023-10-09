import os
import fnmatch
NULL_CHAR = chr(0)


def filecreate(data, path, filetype):
    if filetype == 'w':
        with open(path, 'w') as f:
            f.write(data)
    elif filetype == 'wb':
        with open(path, 'wb') as f:
            encoded_data = data.encode('utf-8')
            f.write(encoded_data)


def write_hid(report_descriptor,placeholder,placeholder2):
    with open('/sys/kernel/config/usb_gadget/iosghgp/functions/hid.usb0/report_desc', 'wb') as fd:
        fd.write(report_descriptor)
        

def init():

    if not os.path.exists('/sys/kernel/config/usb_gadget/iosghgp'):

        print ("Initializing USB Device.")
        os.mkdir('/sys/kernel/config/usb_gadget/iosghgp')
        os.mkdir('/sys/kernel/config/usb_gadget/iosghgp/strings/0x409')
        os.mkdir('/sys/kernel/config/usb_gadget/iosghgp/configs/c.1/')
        os.mkdir('/sys/kernel/config/usb_gadget/iosghgp/configs/c.1/strings/0x409')
        os.mkdir('/sys/kernel/config/usb_gadget/iosghgp/functions/hid.usb0')

        # Creating device
        filecreate('0x1d6b', '/sys/kernel/config/usb_gadget/iosghgp/idVendor', 'wb')
        filecreate(
            '0x0104', '/sys/kernel/config/usb_gadget/iosghgp/idProduct', 'wb')
        filecreate(
            '0x0100', '/sys/kernel/config/usb_gadget/iosghgp/bcdDevice', 'wb')
        filecreate('0x0200', '/sys/kernel/config/usb_gadget/iosghgp/bcdUSB', 'wb')
        filecreate(
            '0xef', '/sys/kernel/config/usb_gadget/iosghgp/bDeviceClass', 'wb')
        filecreate(
            '0x02', '/sys/kernel/config/usb_gadget/iosghgp/bDeviceSubClass', 'wb')
        filecreate(
            '0x01', '/sys/kernel/config/usb_gadget/iosghgp/bDeviceProtocol', 'wb')

        filecreate(
            'Ver1.2', '/sys/kernel/config/usb_gadget/iosghgp/strings/0x409/serialnumber', 'w')
        filecreate('Jose Phillips',
                   '/sys/kernel/config/usb_gadget/iosghgp/strings/0x409/manufacturer', 'w')
        filecreate('iOS GH Live Guitar',
                   '/sys/kernel/config/usb_gadget/iosghgp/strings/0x409/product', 'w')
        filecreate('Config 1: ECM network',
                   '/sys/kernel/config/usb_gadget/iosghgp/configs/c.1/strings/0x409/configuration', 'w')
        filecreate(
            '250', '/sys/kernel/config/usb_gadget/iosghgp/configs/c.1/MaxPower', 'w')
        filecreate(
            '1', '/sys/kernel/config/usb_gadget/iosghgp/functions/hid.usb0/protocol', 'w')
        filecreate(
            '1', '/sys/kernel/config/usb_gadget/iosghgp/functions/hid.usb0/subclass', 'w')
        filecreate(
            '8', '/sys/kernel/config/usb_gadget/iosghgp/functions/hid.usb0/report_length', 'w')

        jybuffer = b'\x05\x01\x09\x04\xa1\x01\x15\x81\x25\x7f\x09\x01\xa1\x00\x09\x30\x09\x31\x75\x08\x95\x02\x81\x02\xc0\x05\x09\x19\x01\x29\x10\x15\x00\x25\x01\x75\x01\x95\x10\x81\x02\xc0'
        write_hid(
            jybuffer, '/sys/kernel/config/usb_gadget/iosghgp/functions/hid.usb0/report_desc', 'wb')

        os.symlink('/sys/kernel/config/usb_gadget/iosghgp/functions/hid.usb0',
                   '/sys/kernel/config/usb_gadget/iosghgp/configs/c.1/hid.usb0')

        dirlist = os.listdir('/sys/class/udc')
        pattern = "*.usb"
        for entry in dirlist:
            if fnmatch.fnmatch(entry, pattern):
                filecreate(
                    entry, '/sys/kernel/config/usb_gadget/iosghgp/UDC', 'w')
        print ("USB Device initialized succesfully.")
    else:
        print ("Device is already initialized.")



def gamepadpress(key):
    with open('/dev/hidg0', 'wb') as fd:
      fd.write(key)
        

def process(ba_rawmessage):

    rawmessage = bytes(ba_rawmessage)
    keys = bytes([rawmessage[0]])
    strum_hexdata = bytes([rawmessage[4]])
    buttons = bytes([rawmessage[1]])
    tilt_hexdata = bytes([rawmessage[5]])
    tilt_axis = bytes([rawmessage[19]])
    whammybar_axis = bytes([rawmessage[6]])

    ''' Strum Data 0xff Strum UP
        0x80 no Strum
        0x00 Strum Down
    '''

    # Strum Up is 0xff
    if strum_hexdata == b'\xff':
        keys = bytes([keys[0] + 0x80])


    # Strum Down is 0x00
    if strum_hexdata == b'\x00':
        keys = bytes([keys[0] + 0x40])

    ''' Tilt Data
        0xFF Tilt UP
        0X80 no Tilt
        0X00 Tilt Down
    '''
    # Add Tilt_hexdata mixed with buttons information
    if tilt_hexdata == b'\xff':
        buttons = bytes([buttons[0] + 0x40])
    elif tilt_hexdata == b'\x00':
        buttons = bytes([buttons[0] + 0x20])

    # Concatenate the bytes
    concatenated_bytes = whammybar_axis + tilt_axis + keys + buttons

    # Send all the state to the device
    gamepadpress(concatenated_bytes)

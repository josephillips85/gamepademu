import os
import fnmatch
import sys
NULL_CHAR = chr(0)
last_state_keys = []
last_state_strum = []
last_state_tilt = 0
reload(sys)
sys.setdefaultencoding("ISO-8859-1")


def filecreate(data, path, filetype):

    f = open(path, filetype)
    f.write(data)
    f.close()


def init():

    if not os.path.exists('/sys/kernel/config/usb_gadget/iosghgp'):

        print "Initializing USB Device."
        os.mkdir('/sys/kernel/config/usb_gadget/iosghgp')
        os.mkdir('/sys/kernel/config/usb_gadget/iosghgp/strings/0x409')
        os.mkdir('/sys/kernel/config/usb_gadget/iosghgp/configs/c.1/')
        os.mkdir('/sys/kernel/config/usb_gadget/iosghgp/configs/c.1/strings/0x409')
        os.mkdir('/sys/kernel/config/usb_gadget/iosghgp/functions/hid.usb0')

        # Creating device
        filecreate('0x1d6b', '/sys/kernel/config/usb_gadget/iosghgp/idVendor', 'w')
        filecreate(
            '0x0104', '/sys/kernel/config/usb_gadget/iosghgp/idProduct', 'w')
        filecreate(
            '0x0100', '/sys/kernel/config/usb_gadget/iosghgp/bcdDevice', 'w')
        filecreate('0x0200', '/sys/kernel/config/usb_gadget/iosghgp/bcdUSB', 'w')
        filecreate(
            '01234567', '/sys/kernel/config/usb_gadget/iosghgp/strings/0x409/serialnumber', 'w')
        filecreate('Jose Phillips',
                   '/sys/kernel/config/usb_gadget/iosghgp/strings/0x409/manufacturer', 'w')
        filecreate('iOS GH Live Guitar',
                   '/sys/kernel/config/usb_gadget/iosghgp/strings/0x409/product', 'w')
        filecreate('Config 1: ECM network',
                   '/sys/kernel/config/usb_gadget/iosghgp/configs/c.1/strings/0x409/configuration', 'w')
        filecreate(
            '250', '/sys/kernel/config/usb_gadget/iosghgp/configs/c.1/MaxPower', 'w')

        filecreate(
            '0', '/sys/kernel/config/usb_gadget/iosghgp/functions/hid.usb0/protocol', 'w')
        filecreate(
            '0', '/sys/kernel/config/usb_gadget/iosghgp/functions/hid.usb0/subclass', 'w')
        filecreate(
            '8', '/sys/kernel/config/usb_gadget/iosghgp/functions/hid.usb0/report_length', 'w')

        kbbuffer = '\x05\x01\x09\x04\xa1\x01\x15\x81\x25\x7f\x09\x01\xa1\x00\x09\x30\x09\x31\x75\x08\x95\x02\x81\x02\xc0\x05\x09\x19\x01\x29\x13\x15\x00\x25\x01\x75\x01\x95\x08\x81\x02\xc0'
        filecreate(
            kbbuffer, '/sys/kernel/config/usb_gadget/iosghgp/functions/hid.usb0/report_desc', 'wb')

        os.symlink('/sys/kernel/config/usb_gadget/iosghgp/functions/hid.usb0',
                   '/sys/kernel/config/usb_gadget/iosghgp/configs/c.1/hid.usb0')

        dirlist = os.listdir('/sys/class/udc')
        pattern = "*.usb"
        for entry in dirlist:
            if fnmatch.fnmatch(entry, pattern):
                filecreate(
                    entry, '/sys/kernel/config/usb_gadget/iosghgp/UDC', 'w')
        print "USB Device initialized succesfully."
    else:
        print "Device is already initialized."


def gamepadpress(key):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(key.encode())


def sumbytes(allbytes):
    return bytes('%02X' % (sum(map(ord, allbytes)) % 256))


def process(ba_rawmessage):
    global last_state_keys
    global last_state_strum
    global last_state_tilt
    rawmessage = bytes(ba_rawmessage)
    keys = rawmessage[0]
    strum_hexdata = rawmessage[4]
    buttons = rawmessage[1]
    tilt_hexdata = rawmessage[5]
    tilt_axis = rawmessage[19]
    whammybar_axis = rawmessage[6]

    ''' Strum Data 0xff Strum UP
	0x80 no Strum
	0x00 Strum Down
	'''

    # Strum Up is 0xff
    if strum_hexdata == '\xff':
        sum = sumbytes(keys + '\x80')
        keys2 = str(sum)
        keys = eval(r"'\x" + keys2 + "'")

    # Strum Down is 0x00
    if strum_hexdata == '\x00':
        sum = sumbytes(keys + '\x40')
        keys2 = str(sum)
        keys = eval(r"'\x" + keys2 + "'")

    ''' Tilt Data
	0xFF Tilt UP
	0X80 no Tilt
	0X00 Tilt Down
	'''

    if tilt_hexdata == '\xff':
        tilt_hexdata = '\x02'
    elif tilt_hexdata == '\x00':
        tilt_hexdata = '\x04'
    elif tilt_hexdata == '\x80':
        tilt_hexdata = '\x00'

    # Send all the the state to device
    gamepadpress(whammybar_axis + tilt_axis + keys + buttons + tilt_hexdata)

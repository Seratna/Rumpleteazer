from pathlib import Path
from typing import Union


def get_keyboard_descriptor():
    """
    this is a HID keyboard report descriptor from a 3-part tutorial:
    https://www.rmedgar.com/blog/using-rpi-zero-as-keyboard-setup-and-device-definition/
    https://www.rmedgar.com/blog/using-rpi-zero-as-keyboard-report-descriptor/
    https://www.rmedgar.com/blog/using-rpi-zero-as-keyboard-send-reports/
    """
    return (
        b'\x05\x01'  # USAGE_PAGE (Generic Desktop)
        b'\x09\x06'  # USAGE (Keyboard)
        b'\xa1\x01'  # COLLECTION (Application)
        b'\x05\x07'  # ..USAGE_PAGE (Key Codes)
        b'\x19\xe0'  # ..USAGE_MINIMUM (224)
        b'\x29\xe7'  # ..USAGE_MAXIMUM (231)
        b'\x15\x00'  # ..LOGICAL_MINIMUM (0)
        b'\x25\x01'  # ..LOGICAL_MAXIMUM (1)
        b'\x75\x01'  # ..REPORT_SIZE (1)
        b'\x95\x08'  # ..REPORT_COUNT (8)
        b'\x81\x02'  # ..INPUT (Data,Var,Abs)  # Modifier byte
        
        b'\x95\x01'  # ..REPORT_COUNT (1)
        b'\x75\x08'  # ..REPORT_SIZE (8)
        b'\x81\x03'  # ..INPUT (Constant)  # Reserved byte
        
        b'\x95\x05'  # ..REPORT_COUNT (5)
        b'\x75\x01'  # ..REPORT_SIZE (1)
        b'\x05\x08'  # ..USAGE_PAGE (LEDs)
        b'\x19\x01'  # ..USAGE_MINIMUM (1)
        b'\x29\x05'  # ..USAGE_MAXIMUM (5)
        b'\x91\x02'  # ..OUTPUT (Data,Var,Abs)  # LED report
        
        b'\x95\x01'  # ..REPORT_COUNT (1)
        b'\x75\x03'  # ..REPORT_SIZE (3)
        b'\x91\x03'  # ..OUTPUT (Constant)  # padding
        
        b'\x95\x06'  # ..REPORT_COUNT (6)
        b'\x75\x08'  # ..REPORT_SIZE (8)
        b'\x15\x00'  # ..LOGICAL_MINIMUM (0)
        b'\x25\x65'  # ..LOGICAL_MAXIMUM (101)
        b'\x05\x07'  # ..USAGE_PAGE (Key Codes)
        b'\x19\x00'  # ..USAGE_MINIMUM (0)
        b'\x29\x65'  # ..USAGE_MAXIMUM (101)  # keys
        
        b'\x81\x00'  # ..INPUT (Data,Array)
        b'\xc0'  # END_COLLECTION
    )


def get_mouse_descriptor():
    """
    this is the report descriptor of Logitech Gaming Mouse G900
    """
    return (
        b'\x05\x01'  # USAGE_PAGE (Generic Desktop)
        b'\x09\x02'  # USAGE (Mouse)
        b'\xa1\x01'  # COLLECTION (Application)
        b'\x09\x01'  # ..USAGE (Pointer)
        b'\xa1\x00'  # ..COLLECTION (Physical)
        b'\x05\x09'  # ....USAGE_PAGE (Button)
        b'\x19\x01'  # ....USAGE_MINIMUM (Button 1)
        b'\x29\x10'  # ....USAGE_MAXIMUM (Button 16)
        b'\x15\x00'  # ....LOGICAL_MINIMUM (0)
        b'\x25\x01'  # ....LOGICAL_MAXIMUM (1)
        b'\x95\x10'  # ....REPORT_COUNT (16)
        b'\x75\x01'  # ....REPORT_SIZE (1)
        b'\x81\x02'  # ....INPUT (Data,Var,Abs)
        
        b'\x05\x01'  # ....USAGE_PAGE (Generic Desktop)
        b'\x16\x01\x80'  # ....LOGICAL_MINIMUM (-32767)
        b'\x26\xff\x7f'  # ....LOGICAL_MAXIMUM (32767)
        b'\x75\x10'  # ....REPORT_SIZE (16)
        b'\x95\x02'  # ....REPORT_COUNT (2)
        b'\x09\x30'  # ....USAGE (X)
        b'\x09\x31'  # ....USAGE (Y)
        b'\x81\x06'  # ....INPUT (Data,Var,Rel)
        
        b'\x15\x81'  # ....LOGICAL_MINIMUM (-127)
        b'\x25\x7f'  # ....LOGICAL_MAXIMUM (127)
        b'\x75\x08'  # ....REPORT_SIZE (8)
        b'\x95\x01'  # ....REPORT_COUNT (1)
        b'\x09\x38'  # ....USAGE (Wheel)
        b'\x81\x06'  # ....INPUT (Data,Var,Rel)
        
        b'\x05\x0c'  # ....USAGE_PAGE (Consumer Devices)
        b'\x0a\x38\x02'  # ....USAGE (AC Pan)
        b'\x95\x01'  # ....REPORT_COUNT (1)
        b'\x81\x06'  # ....INPUT (Data,Var,Rel)
        
        b'\xc0'  # ..END_COLLECTION
        b'\xc0'  # END_COLLECTION
    )


def write(content: Union[str, bytes], path: Path):
    if isinstance(content, str):
        with open(path, 'w') as file:
            file.write(content)
    elif isinstance(content, bytes):
        with open(path, 'wb') as file:
            file.write(content)
    else:
        raise NotImplementedError


def setup():
    gadget_name = 'pi_mouse'
    gadget_dir = Path(f'/sys/kernel/config/usb_gadget', gadget_name)
    gadget_dir.mkdir(parents=True)

    # Add basic information
    write('0x0104', Path(gadget_dir, 'bcdDevice'))  # Version 1.0.4
    write('0x0200', Path(gadget_dir, 'bcdUSB'))  # USB 2.0
    write('0x00', Path(gadget_dir, 'bDeviceClass'))
    write('0x00', Path(gadget_dir, 'bDeviceSubClass'))
    write('0x00', Path(gadget_dir, 'bDeviceProtocol'))

    write('0x40', Path(gadget_dir, 'bMaxPacketSize0'))  # 64
    write('0xc081', Path(gadget_dir, 'idProduct'))
    write('0x046d', Path(gadget_dir, 'idVendor'))  # Logitech, Inc.

    # Create English locale
    en_dir = Path(gadget_dir, 'strings/0x409')
    en_dir.mkdir(parents=True)

    write('Logitech', Path(en_dir, 'manufacturer'))
    write('Gaming Mouse G900', Path(en_dir, 'product'))
    write('3.1415926535897932', Path(en_dir, 'serialnumber'))

    # Create HID function
    hid_dir = Path(gadget_dir, 'functions/hid.usb0')
    hid_dir.mkdir(parents=True)

    write('1', Path(hid_dir, 'subclass'))  # Boot Interface Subclass
    write('2', Path(hid_dir, 'protocol'))  # Mouse
    write('8', Path(hid_dir, 'report_length'))  # 8-byte reports
    write(get_keyboard_descriptor(), Path(hid_dir, 'report_desc'))

    # Create configuration
    config_dir = Path(gadget_dir, 'configs/c.1')
    config_dir.mkdir(parents=True)
    config_en_dir = Path(config_dir, 'strings/0x409')
    config_en_dir.mkdir(parents=True)

    write('0xa0', Path(config_dir, 'bmAttributes'))
    write('498', Path(config_dir, 'MaxPower'))  # 498 mA
    write('configuration', Path(config_en_dir, 'configuration'))

    # Link HID function to configuration
    Path(config_dir, hid_dir.name).symlink_to(hid_dir)

    # Enable gadget
    write('\n'.join([p.name for p in Path('/sys/class/udc').iterdir()]),
          Path(gadget_dir, 'UDC'))


def main():
    setup()


if __name__ == '__main__':
    main()

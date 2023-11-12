# nec-pos-printer
Connect NEC-POS-Printer without a driver. 

This is the research project, when my NEC TWIN POS were obsolete, and I need to use Linux instead of Windows.
NEC could do this for us, so I started debug the message.

Concept is to use communication direct to the USB in stead of Drivers, because they could provide the drivers for Linux.

Library was LIBUSB.

First tried in Python but didn't work . 

Thanks for this  "https://github.com/FD-/usb-toolbox" project made my life easier.

I used his code and add just one module to test NEC printer.

used FD-USB-toolsbox command to connect and open the USB and develop replay packet to test "test-nec", it's worked!

Result in 
  /cpp_lib_usb

After C++ work , I captured pcab in /datalog , and found some defected in "pyusb", so I fixed in "/usb/core.py".

Result in 
  /py_lib_usb/usb/core.py

And develop some test python, now it's worked.

NEC Printers didn't communicate with the host using ESC/POS and I found that they use binary bits to print.

416 bits (== dots) per lines. and staight forward.

Headers for print are,

[ 0x1b 0x63 0x30 0x02 0x1a 0x2e 0x30 0xa0 0x01 A B ]

A, B  is lengh
for example
  A=0x1b , B=0x00
  length = 001b = 27
  lenght in bits   =   27 * 416 bits = 11232 bits
  convert to bytes =   27 * 416 / 8 bytes = 1404 bytes
  
 

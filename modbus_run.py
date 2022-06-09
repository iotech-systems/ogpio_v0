#!/usr/bin/env python3

import time, serial, sys
from core.modbusBoard import modbusBoard
from devices.lctech4chModbus import lctech4chModbus


print("\n\n\t--[ modbus-scan ]--")

_prt = ""
_bdr = ""
_par = ""

if len(sys.argv) == 4:
   _prt = sys.argv[1]
   _bdr = sys.argv[2]
   _par = sys.argv[3]

# - - - set - - -
if _prt == "":
   _port = input("\tport: ")
   if _port == "":
      _port = "/dev/ttyUSB0"
else:
   _port = _prt
# - - - set - - -
if _bdr == "":
   _baudrate = input("\tbaudrate: ")
   if _baudrate in [None, ""]:
      _baudrate = 9600
   else:
      _baudrate = int(_baudrate)
else:
   _baudrate = int(_bdr)
# - - - set - - -
if _par == "":
   _parity = input("\tparity: ")
   if _parity == "":
      _parity = "N"
else:
   _parity = _par

msg = f"\n\tusing: [ port: {_port}; baudrate: {_baudrate}; parity: {_parity}; ]\n"
print(msg)


# (ser: serial.Serial, unit_adr: int, relay: int, val: int)
def main():
   ser = serial.Serial(port=_port, baudrate=_baudrate, parity=_parity)
   modbus_adr = 8
   device: modbusBoard = lctech4chModbus(ser_port=ser, modbus_adr=modbus_adr)
   if device.set_bus_address(0, modbus_adr):
      print(f"New Modbus address set: {modbus_adr}")
   else:
      print(f"New Modbus address NOT set: {modbus_adr}")
      exit(1)
   # -- loop --
   while True:
      time.sleep(4.0)
      for chl in range(0, 4):
         device.set_channel(chl, False)
         time.sleep(1.0)
      time.sleep(4.0)
      for chl in range(0, 4):
         device.set_channel(chl, True)
         time.sleep(1.0)


# -- start --
if __name__ == "__main__":
   main()

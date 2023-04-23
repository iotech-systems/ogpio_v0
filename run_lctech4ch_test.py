#!/usr/bin/env python3

import time, serial, sys
from interfaces.modbusBoard import modbusBoard
from boards.lctech4chModbus import lctech4chModbus


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
   state = False
   ser = serial.Serial(port=_port, baudrate=_baudrate, parity=_parity)
   while True:
      for mb_adr in [4, 8]:
         device: modbusBoard = lctech4chModbus(ser_port=ser, modbus_adr=mb_adr)
         # if device.set_bus_address(255, mb_adr):
         #    print(f"New Modbus address set: {mb_adr}")
         # else:
         #    print(f"New Modbus address NOT set: {mb_adr}")
         #    exit(1)
         # # -- loop --
         for chl in range(0, 4):
            ser.write("HELLO".encode("utf-8"))
            time.sleep(0.1)
            device.set_channel(chl, state)
            time.sleep(2.0)
      state = not state


# -- start --
if __name__ == "__main__":
   main()

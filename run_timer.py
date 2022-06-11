#!/usr/bin/env python3

import serial, sys, time
from interfaces.modbusBoard import modbusBoard
from boards.lctech4chModbus import lctech4chModbus
from core.clock import clock

MODBUS_ADR = 8

_src = "this script full path"
_prt = ""   # port
_bdr = ""   # baudrate
_par = ""   # parity
_chl = ""   # relay numer
_ont = ""   # on time
_oft = ""   # off time

if len(sys.argv) == 7:
   _src = sys.argv[0]
   _prt = sys.argv[1]
   _bdr = int(sys.argv[2])
   _par = sys.argv[3]
   _chl = int(sys.argv[4])
   _ont = sys.argv[5]
   _oft = sys.argv[6]
else:
   print("-- [ bad argv ] --")
   exit(1)

if not clock.is_good_time(_ont):
   exit(1)

if not clock.is_good_time(_oft):
   exit(1)

print(f"\n\n\t- - [ run-timer ] - -\n\t- - [ {_src} ] - -")
print(f"\n\tusing: [ port: {_prt}; baudrate: {_bdr}; parity: {_par}; ]\n")


def set_channel(ser: serial.Serial, chnl: int, ont: str, oft: str):
   board: modbusBoard = lctech4chModbus(ser_port=ser, modbus_adr=chnl)
   chnl_state: bool = clock.get_state(ont, oft)
   board.set_channel(chnl, chnl_state)

# (ser: serial.Serial, unit_adr: int, relay: int, val: int)
def main():
   ser = serial.Serial(port=_prt, baudrate=_bdr, parity=_par)
   board: modbusBoard = lctech4chModbus(ser_port=ser, modbus_adr=MODBUS_ADR)
   board.set_bus_address(0, MODBUS_ADR)
   # -- loop --
   while True:
      # -- use global variables --
      set_channel(ser, _chl, _ont, _oft)
      time.sleep(8.0)


# -- start --
if __name__ == "__main__":
   main()

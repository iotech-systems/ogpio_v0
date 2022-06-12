#!/usr/bin/env python3

import serial, sys, time
from interfaces.modbusBoard import modbusBoard
from boards.lctech4chModbus import lctech4chModbus
from core.clock import clock
from core.locationTxtInfo import locationTxtInfo
from core.sunclock import *

MODBUS_ADR = 8
LOC_INFO: locationTxtInfo = locationTxtInfo("location.txt")
LOC_INFO.load()

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
   # -- could be day part names --
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


def set_channel(ser: serial.Serial, mb_adr: int, chnl: int, ont: str, oft: str):
   # -- run --
   sun_clock = sunClock(LOC_INFO)
   board: modbusBoard = lctech4chModbus(ser_port=ser, modbus_adr=mb_adr)
   if ont in DAY_PARTS:
      ont = sun_clock.get_time(ont)
   if oft in DAY_PARTS:
      oft = sun_clock.get_time(oft)
   # -- run --
   chnl_state: bool = clock.get_state(ont, oft)
   print(f"\t[ new chnl_state: {chnl_state} ]")
   board.set_channel(chnl, chnl_state)

# (ser: serial.Serial, unit_adr: int, relay: int, val: int)
def main():
   ser = serial.Serial(port=_prt, baudrate=_bdr, parity=_par)
   board: modbusBoard = lctech4chModbus(ser_port=ser, modbus_adr=MODBUS_ADR)
   print(f"\n- - - [ SETTING MODBUS_ADR: {MODBUS_ADR} ] - - -\n")
   board.set_bus_address(0, MODBUS_ADR)
   print("\n- - - [ SETTING ALL OFF ] - - -\n")
   board.set_all_channels(False)
   time.sleep(4.0)
   # -- loop --
   while True:
      # -- use global variables --
      set_channel(ser, MODBUS_ADR, _chl, _ont, _oft)
      time.sleep(8.0)


# -- start --
if __name__ == "__main__":
   main()

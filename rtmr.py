#!/usr/bin/env python3
import os.path

import serial, sys, time
from interfaces.modbusBoard import modbusBoard
from boards.lctech4chModbus import lctech4chModbus
from core.clock import clock
from core.sunclock import *
from utils.sysUtils import sysUtils
from datatypes.timetableXml import timetableXml
from datatypes.modbusInfo import modbusInfo
from datatypes.ttyDev import ttyDev


MODBUS_ADR = 8
LOC_INFO: locationTxtInfo = locationTxtInfo("location.txt")
LOC_INFO.load()

_src_file = sys.argv[0]
_timetable_xml: str = ""

if len(sys.argv) == 1:
   _timetable_xml = "rtmr_timetable.xml"
elif len(sys.argv) == 2:
   _timetable_xml = sys.argv[1]
else:
   print("-- [ bad argv ] --")
   exit(1)

if not os.path.exists(_timetable_xml):
   print(f"\n\t[ FileNotFound: {_timetable_xml} ]\n")
   exit(1)

print(f"\n\n\t-- [ run-timer ] - -\n\t- - [ {_src_file} ] - -")

# -- load xml config --
ttXML: timetableXml = timetableXml(_timetable_xml)
if ttXML.load() != 0:
   print(f"UnableToLoadXmlFile: {_timetable_xml}")
   exit(1)


# -- load modbus node --
mbInfo: modbusInfo = ttXML.get_modbusInfo()
print(f"\n\t-- [ ttydev.buff: {mbInfo.ttydev.buff} ] --\n")


def get_comm(mb_adr: int, bdr: int, par: str) -> [None, serial.Serial]:
   # -- auto detect com port --
   ser: [None, serial.Serial] = None
   ports = sysUtils.usbPorts()
   for port in ports:
      try:
         ser = serial.Serial(port.device, baudrate=bdr, parity=par)
         if lctech4chModbus.ping(ser, mb_adr):
            break
         ser = None
      except Exception as e:
         print(e)
   # -- return --
   return ser

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
   # -- --
   port: ttyDev = mbInfo.ttydev
   if port.dev == "auto":
      ser = get_comm(mb_adr=mbInfo.address, bdr=port.baud, par=port.parity)
      if ser is None:
         exit(22)
   else:
      ser = serial.Serial(port=port.dev, baudrate=port.baud, parity=port.parity)
   # -- --
   print(f"\n\tusing ser. port: {ser}\n")
   board: modbusBoard = lctech4chModbus(ser_port=ser, modbus_adr=mbInfo.address)
   print(f"\n- - - [ SETTING MODBUS_ADR: {mbInfo.address} ] - - -\n")
   board.set_bus_address(0, mbInfo.address)
   print("\n- - - [ SETTING ALL OFF ] - - -\n")
   board.set_all_channels(False)
   time.sleep(4.0)
   # -- loop --
   while True:
      # -- for each gpio --
      for gpio in mbInfo.gpios:
         print(gpio)
         set_channel(ser, mbInfo.address, _chl, _ont, _oft)
      # -- sleep a bit --
      time.sleep(16.0)


# -- start --
if __name__ == "__main__":
   main()

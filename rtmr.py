#!/usr/bin/env python3

import setproctitle
import serial, sys, time, os.path
from interfaces.modbusBoard import modbusBoard
from boards.lctech4chModbus import lctech4chModbus
from core.clock import clock
from core.sunclock import *
from utils.sysUtils import sysUtils
from datatypes.timetableXml import timetableXml
from datatypes.modbusInfo import modbusInfo
from datatypes.modbusGPIO import modbusGPIO
from core.fileMonitor import fileMonitor
from datatypes.ttyDev import ttyDev


ttXML = None
MB_INFO = None
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


def on_conf_change():
   print("on_conf_change")


fileMon: fileMonitor = fileMonitor(_timetable_xml)
fileMon.set_callback(None)
fileMon.start()

print(f"\n\n\t-- [ run-timer ] - -\n\t- - [ {_src_file} ] - -")


def load_xml_conf_file():
   # -- load xml config --
   global ttXML
   ttXML = timetableXml(_timetable_xml)
   if ttXML.load() != 0:
      print(f"UnableToLoadXmlFile: {_timetable_xml}")
      exit(1)
   # -- load modbus node --
   global MB_INFO
   MB_INFO = ttXML.get_modbusInfo()
   print(f"\n\t-- [ ttydev.buff: {MB_INFO.ttydev.buff} ] --\n")
   MB_INFO.load_gpios()

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
   try:
      ont_offset: int = 0
      oft_offset: int = 0
      # -- test for time offset --
      m_ont = re.match(RGX, ont)
      m_oft = re.match(RGX, oft)
      # -- --
      if (m_ont is not None) and (len(m_ont.groups()) == 2):
         g0_ont, g1_ont = m_ont.groups()
         ont = g0_ont.strip()
         ont_offset = int(g1_ont.strip())
      if (m_oft is not None) and (len(m_oft.groups()) == 2):
         g0_oft, g1_oft = m_ont.groups()
         oft = g0_oft.strip()
         oft_offset = int(g1_oft.strip())
      # -- --
      sun_clock = sunClock(LOC_INFO)
      if ont in DAY_PARTS:
         ont = sun_clock.get_time(ont, ont_offset)
      if oft in DAY_PARTS:
         oft = sun_clock.get_time(oft, oft_offset)
      # - - - run - - -
      chnl_state: bool = clock.get_state(ont, oft)
      print(f"\t[ new chnl_state: {chnl_state} ]")
      board: modbusBoard = lctech4chModbus(ser_port=ser, modbus_adr=mb_adr)
      board.set_channel(chnl, chnl_state)
   except Exception as e:
      print(e)

def per_gpio(ser: serial.Serial, gpio: modbusGPIO):
   if not gpio.enabled:
      return
   print(gpio)
   set_channel(ser, MB_INFO.address, gpio.id, gpio.on, gpio.off)
   time.sleep(2.0)

def while_loop(ser: serial.Serial):
   print("\n-- [ while_loop ] --\n")
   while True:
      if fileMon.fileChanged:
         load_xml_conf_file()
      # -- for each gpio --
      mb_info: modbusInfo = MB_INFO
      for gpio in mb_info.gpios:
         per_gpio(ser, gpio)
      # -- sleep a bit --
      time.sleep(8.0)

def main():
   load_xml_conf_file()
   port: ttyDev = MB_INFO.ttydev
   if port.dev == "auto":
      ser = get_comm(mb_adr=MB_INFO.address, bdr=port.baud, par=port.parity)
      if ser is None:
         exit(22)
   else:
      ser = serial.Serial(port=port.dev, baudrate=port.baud, parity=port.parity)
   # -- --
   print(f"\n\tusing ser. port: {ser}\n")
   board: modbusBoard = lctech4chModbus(ser_port=ser, modbus_adr=MB_INFO.address)
   print(f"\n- - - [ SETTING MODBUS_ADR: {MB_INFO.address} ] - - -\n")
   board.set_bus_address(0, MB_INFO.address)
   print("\n- - - [ SETTING ALL OFF ] - - -\n")
   board.set_all_channels(False)
   time.sleep(4.0)
   # -- loop --
   while_loop(ser)


# -- start --
if __name__ == "__main__":
   PROC_NAME = "ogpio::rtmr"
   setproctitle.setproctitle(PROC_NAME)
   main()

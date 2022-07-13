
import os.path
import typing as t
import xml.etree.ElementTree as et
from datatypes.modbusInfo import modbusInfo
from core.sunclock import *
from core.clock import clock
from datatypes.gpioState import gpioState


class timetableXml(object):

   def __init__(self, path: str):
      self.path: str = path
      self.xml: et.ElementTree = None

   def load(self) -> int:
      if not os.path.exists(self.path):
         return 1
      self.xml: et.ElementTree = et.parse(self.path)
      return 0

   def get_modbusInfo(self) -> modbusInfo:
      elmt: et.Element = self.xml.find("modbus")
      return modbusInfo(elmt)

   def pprint(self):
      xpath = "modbus/gpio"
      gpios: t.List[et.Element] = self.xml.findall(xpath)
      LOC_INFO: locationTxtInfo = locationTxtInfo("location.txt")
      LOC_INFO.load()
      sclk = sunClock(loc_info=LOC_INFO)
      clk = clock()
      # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      # <gpio enabled="on" id="0" lbl="CH1" on="sunset" off="sunrise" note="kasetony" />
      arr = [f"\n\t{sclk}"]
      for gpio in gpios:
         _id = gpio.attrib["id"]
         lbl = gpio.attrib["lbl"]
         onStr = gpio.attrib["on"]
         offStr = gpio.attrib["off"]
         enb = "{:3s}".format(gpio.attrib["enabled"])
         gpioCalc = gpioState(onStr, offStr)
         _on = "{:20s}".format(f"{offStr}/{gpioCalc.timeOn}")
         _off = "{:20s}".format(f"{offStr}/{gpioCalc.timeOff}")
         state = gpioCalc.calc_current_state()
         state = "1" if state else "0"
         _msg = f"\n\tGPIO [ enabled: {enb} | id: {_id} | calc_state: {state} |" \
            f" lbl: {lbl} | on: {_on} | off: {_off} ]"
         arr.append(_msg)
      # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      # -- print buffer --
      tbl = "".join(arr)
      return f"\n\t- - - [ timetable ] - - -\n\tfile: {self.path}\n{tbl}\n\n"

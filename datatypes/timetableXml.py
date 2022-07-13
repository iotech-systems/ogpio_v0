
import os.path
import typing as t
import xml.etree.ElementTree as et
from datatypes.modbusInfo import modbusInfo
from core.sunclock import *
from core.clock import clock


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
      # -- --
      arr = [f"\n\t{sclk}"]
      for gpio in gpios:
         # <gpio enabled="on" id="0" lbl="CH1" on="sunset" off="sunrise" note="kasetony" />
         enb = "{:3s}".format(gpio.attrib["enabled"]); id = gpio.attrib["id"]
         lbl = gpio.attrib["lbl"]; ton = gpio.attrib["on"]
         toff = gpio.attrib["off"]; note = gpio.attrib["note"]
         dton = sclk.get_time_v1(ton); dtoff = sclk.get_time_v1(toff)
         state = "1" if (clock.get_state(dton, dtoff)) else "0"
         _msg = f"\n\tGPIO [ enabled: {enb} | id: {id} | calc_state: {state} | lbl: {lbl}" \
            f" | on: {ton} / {dton} | off: {toff} / {dtoff} | note: {note} ]"
         arr.append(_msg)
      # -- print buffer --
      tbl = "".join(arr)
      return f"\n\t- - - [ timetable ] - - -\n\tfile: {self.path}\n{tbl}\n\n"

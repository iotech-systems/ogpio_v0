
import typing as t, serial
import xml.etree.ElementTree as et
from serial.tools import list_ports


class sysUtils:

   @staticmethod
   def usbPorts():
      ports = list_ports.comports()
      return [p for p in ports if ("USB" in p.name.upper())]

   @staticmethod
   def dumpTimetable(xmlConf: et.Element):
      xpath = "modbus/gpio"
      gpios: t.List[et.Element] = xmlConf.findall(xpath)
      filepath = ""
      buff = f"""
         - - - [ timetable ] - - -
            file: {filepath}
            
      """
      print(buff)

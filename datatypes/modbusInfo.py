
import typing as t
import xml.etree.ElementTree as et
from datatypes.ttyDev import ttyDev
from datatypes.modbusGPIO import modbusGPIO


class modbusInfo(object):

   def __init__(self, e: et.Element):
      self.elmt: et.Element = e
      self.address: int = int(self.elmt.attrib["address"])
      self.ttydev: ttyDev = ttyDev(self.elmt.attrib["ttydev"])
      self.gpios: t.List[modbusGPIO] = []
      self.load_gpios()

   def load_gpios(self):
      xpath: str = "modbus/gpio"
      lst: t.List[et.Element] = self.elmt.findall(xpath)
      print(f"lst: {lst}")
      for elmt in lst:
         print(elmt)

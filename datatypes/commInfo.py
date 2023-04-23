
import typing as t
import xml.etree.ElementTree as et
from datatypes.ttyDev import ttyDev
from datatypes.modbusGPIO import modbusGPIO


class commInfo(object):

   def __init__(self, comm: str):
      self.elmt: et.Element = e
      self.address: int = int(self.elmt.attrib["address"])
      self.ttydev: ttyDev = ttyDev(self.elmt.attrib["ttydev"])
      self.gpios: t.List[modbusGPIO] = []
      self.load_gpios()

   def load_gpios(self):
      xpath: str = "gpio[@enabled=\"on\"]"
      lst: t.List[et.Element] = self.elmt.findall(xpath)
      self.gpios.clear()
      for elmt in lst:
         self.gpios.append(modbusGPIO(elmt))

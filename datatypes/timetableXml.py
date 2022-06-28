
import os.path
import xml.etree.ElementTree as et
from datatypes.modbusInfo import modbusInfo


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

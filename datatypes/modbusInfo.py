
import xml.etree.ElementTree as et
from datatypes.ttyDev import ttyDev


class modbusInfo(object):

   def __init__(self, e: et.Element):
      self.elmt: et.Element = e
      self.address: int = int(self.elmt.attrib["address"])
      self.ttydev: ttyDev = ttyDev(self.elmt.attrib["ttydev"])
      self.gpios: [] = None

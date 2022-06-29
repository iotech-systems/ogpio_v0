
import xml.etree.ElementTree as et

"""
   <gpio id="1" on="sunset" off="sunrise" note="kasetony" />
"""
class modbusGPIO(object):

   def __init__(self, elmt: et.Element):
      self.id: int = int(elmt.attrib["id"])
      self.enabled: bool = (elmt.attrib["enabled"] in ["on", "ON", "1"])
      self.on: str = elmt.attrib["on"]
      self.off: str = elmt.attrib["off"]
      self.note: str = elmt.attrib["note"]

   def __str__(self):
      return f"\t[ gpio enabled: {self.enabled} | id: {self.id} | " \
         f"on: {self.on} | off: {self.off} | note: {self.note} ]"

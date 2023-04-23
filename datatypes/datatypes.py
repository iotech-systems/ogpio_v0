
import xml.etree.ElementTree as _et


class scheduleItem(object):

   def __init__(self, elm: _et.Element):
      self.day: str = elm.attrib["day"]
      self.on: str = elm.attrib["on"]
      self.off: str = elm.attrib["off"]

   def __str__(self):
      return f"day: {self.day} | on: {self.on} | off: {self.off}"

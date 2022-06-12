
from serial.tools import list_ports


class sysUtils:

   @staticmethod
   def usbPorts():
      ports = list_ports.comports()
      return [p for p in ports if ("USB" in p.name.upper())]

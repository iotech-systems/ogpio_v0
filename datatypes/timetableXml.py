
import os.path
import typing as t
import xml.etree.ElementTree as et
# from datatypes.modbusInfo import modbusInfo
from datatypes.modbusDevice import modbusDevice
from datatypes.modbusGPIO import modbusGPIO
from core.sunclock import *
from core.clock import clock
from datatypes.gpioState import gpioState
from boards.lctech4chModbus import lctech4chModbus


class timetableXml(object):

   def __init__(self, path: str, locinfo: locationTxtInfo):
      self.LOC_INFO: locationTxtInfo = locinfo
      self.path: str = path
      self.path_mod_time: int = int(os.path.getmtime(self.path))
      self.xml: et.ElementTree = None
      self.MB_DEVICES: t.List[modbusDevice] = []

   def load(self) -> int:
      if not os.path.exists(self.path):
         return 1
      self.xml: et.ElementTree = et.parse(self.path)
      self.__load_mb_devices__()
      return 0

   def reload(self) -> int:
      try:
         m_time: int = int(os.path.getmtime(self.path))
         if self.path_mod_time == m_time:
            return 0
         else:
            self.load()
            self.update_mb_devices()
            self.path_mod_time = m_time
            return 1
      except Exception as e:
         print(e)
         return 2

   def pprint(self):
      # -- print buffer --
      sclk = sunClock(loc_info=self.LOC_INFO)
      sclk_str = f"\n\t{sclk}"
      str_devs: str = "".join([f"\t{str(d)}\n" for d in self.MB_DEVICES])
      return f"\n\t- - - [ timetable ] - - -\n\tfile: {self.path}" \
         f"\n\t{sclk_str}\n\n{str_devs}\n\n"

   def __load_mb_devices__(self):
      # -- -- -- -- -- -- -- --
      xpath = "modbus/device"
      devices: t.List[et.Element] = self.xml.findall(xpath)
      # -- -- -- -- -- -- -- --
      self.MB_DEVICES.clear()
      def __on_device(device: et.Element):
         devid = device.attrib["id"]
         lbl = device.attrib["lbl"]
         adr: int = int(device.attrib["address"])
         ttydev: str = device.attrib["ttydev"]
         print(f"\n[ device: {devid} | lbl: {lbl} | comm: {ttydev} ]")
         # -- create modbus device --
         dev: modbusDevice = \
            modbusDevice(devid=devid, comm=ttydev, mb_adr=adr, lbl=lbl)
         pins: t.List[et.Element] = device.findall("gpio")
         for pin in pins:
            dev.GPIOS.append(modbusGPIO(pin))
         # -- load device --
         self.MB_DEVICES.append(dev)
      # -- -- -- -- -- -- -- --
      for _device in devices:
         __on_device(_device)
      # -- -- -- -- -- -- -- --

   def update_mb_devices(self):
      for mb_dev in self.MB_DEVICES:
         if mb_dev.ttydev.dev != "auto":
            continue
         err, path = lctech4chModbus.get_comm_dev(mb_adr=mb_dev.mb_adr
            , bdr=mb_dev.ttydev.baud, par=mb_dev.ttydev.parity)
         mb_dev.ttydev.dev = path

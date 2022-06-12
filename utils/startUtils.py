
import re, serial
from serial.tools.list_ports_linux import *


LOGS_FLDR = "/opt/iotech/omms/logs"


class startUtils:

   ttyStartLog = f"{LOGS_FLDR}/ttyUSBxStart.log"

   def __init__(self):
      pass

   @staticmethod
   def get_free_ttyUSB(sysPorts: []):
      try:
         with open(startUtils.ttyStartLog, "r") as f:
            buff = f.read()
         # -- find --
         patt = "/dev/ttyUSB[0-9]{1,2}"
         found = re.findall(patt, buff)
         # -- run --
         free_ports = []
         for p in sysPorts:
            s: SysFS = p
            if s.device in found:
               continue
            free_ports.append(s.device)
         # -- return arr --
         return free_ports
      except Exception as e:
         print(e)

   @staticmethod
   def get_closed_comms(comm_ports: []):
      for cp in comm_ports:
         s: SysFS = cp
         # -- try to open comm port --
         ser = serial.Serial(port=s.device)


import time, serial


class rpiHatBoard(object):

   readDelay = 0.200

   def __init__(self):
     pass

   def set_channel(self, chnl: int, val: bool):
      pass

   def read_channel(self, chnl: int):
      pass

   def set_bus_address(self, old_adr: int, new_adr: int):
      pass

   def read_bus_address(self, old_adr: int):
      pass

   def __read__(self) -> [None, bytearray]:
      pass


import serial
from interfaces.rpiHatBoard import rpiHatBoard


class waveshare3chHat(rpiHatBoard):

   def __init__(self):
      super().__init__()

   def set_channel(self, chnl: int, val: bool):
      super().set_channel(chnl, val)

   def read_channel(self, chnl: int):
      super().read_channel(chnl)

   def set_bus_address(self, old_adr: int, new_adr: int):
      super().set_bus_address(old_adr, new_adr)

   def read_bus_address(self, old_adr: int):
      super().read_bus_address(old_adr)

   def __ser_port__(self) -> serial.Serial:
      pass

   def __send__(self, outbuff: bytearray) -> int:
      pass

   def __read__(self) -> [None, bytearray]:
      return super().__read__()

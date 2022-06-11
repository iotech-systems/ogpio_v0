
import time
import serial


class modbusBoard(object):

   readDelay = 0.200

   def __init__(self, ser_port: serial.Serial, modbus_adr: int):
      self.ser_port: serial.Serial = ser_port
      self.modbus_adr: int = modbus_adr

   def set_channel(self, chnl: int, val: bool):
      pass

   def set_all_channels(self, val: bool):
      pass

   def read_channel(self, chnl: int):
      pass

   def set_bus_address(self, old_adr: int, new_adr: int):
      pass

   def read_bus_address(self, old_adr: int):
      pass

   def __ser_port__(self) -> serial.Serial:
      if not self.ser_port.isOpen():
         self.ser_port.open()
      return self.ser_port

   def __send__(self, outbuff: bytearray) -> int:
      ser: serial.Serial = self.__ser_port__()
      print(f" <<< SENDING: {outbuff}")
      cnt = ser.write(outbuff)
      ser.flush()
      # -- sleep 20 ms --
      time.sleep(0.02)
      return cnt

   def __read__(self) -> [None, bytearray]:
      ser: serial.Serial = self.__ser_port__()
      ser.timeout = modbusBoard.readDelay
      inbuff: bytearray = bytearray()
      while True:
         inbuff.extend(ser.read(1))
         if ser.in_waiting == 0:
            break
      print(f" >>>    RESP: {inbuff}")
      # -- return --
      return inbuff

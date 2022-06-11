
import serial
from crcmod.predefined import *
from interfaces.modbusBoard import modbusBoard


class lctech4chModbus(modbusBoard):

   def __init__(self, ser_port: serial.Serial, modbus_adr: int):
      super().__init__(ser_port, modbus_adr)

   def set_channel(self, chnl: int, val: bool):
      data = self.__set_channel_buff__(chnl, val)
      outbuff = self.__add_crc_data__(data)
      super().__send__(outbuff)
      resp: bytearray = super().__read__()
      print(f"resp: {resp}")

   def set_all_channels(self, val: bool):
      """
         5, turn on all relay
         send :FF 0F 00 00 00 08 01 FF 30 1D
         return :FF 0F 00 00 00 08 41 D3
         6,turn off all relay
         send:FF 0F 00 00 00 08 01 00 70 5D
         return :FF 0F 00 00 00 08 41 D3
      """
      if val:
         data: [] = [0x00, 0x0f, 0x00, 0x00, 0x00, 0x08, 0x01, 0xff]
         data[0] = self.modbus_adr
         outbuff = self.__add_crc_data__(bytearray(data))
      else:
         data: [] = [0x00, 0x0f, 0x00, 0x00, 0x00, 0x08, 0x01, 0x00]
         data[0] = self.modbus_adr
         outbuff = self.__add_crc_data__(bytearray(data))
      # -- send & recv --
      super().__send__(outbuff)
      resp: bytearray = super().__read__()
      print(f" >>> RESP: {resp}")

   def read_channel(self, chnl: int):
      pass

   def set_bus_address(self, old_adr: int, new_adr: int):
      """
         Set the device address to 1
            00 10 00 00 00 01 02 00 01 6A 00
         Set the device address to 255
            00 10 00 00 00 01 02 00 FF EB 80
         The 9th byte of the sending frame, 0xFF, is the written device address
      """
      self.modbus_adr = new_adr
      data: () = (0x00, 0x10, 0x00, 0x00, 0x00, 0x01, 0x02, 0x00)
      buff: bytearray = bytearray(data)
      buff.append(self.modbus_adr)
      outbuff: bytearray = self.__add_crc_data__(buff)
      cnt_out: int = self.__send__(outbuff)
      inbuff: bytearray = self.__read__()
      return len(inbuff) == cnt_out

   def read_bus_address(self, old_adr: int):
      pass

   def __set_channel_buff__(self, relay: int, val: bool) -> [None, bytearray]:
      """
         (0xff, 0x05, 0x00, 0x00, 0xFF, 0x00)
      """
      buff: bytearray = bytearray()
      # -- modbus address --
      buff.append(self.modbus_adr)
      # -- modbus function --
      buff.append(0x05)
      # -- relay address --
      buff.extend([0, relay])
      if val:
         buff.extend([0x00, 0x00])
      else:
         buff.extend([0xff, 0x00])
      # -- return buffer --
      return buff

   def __add_crc_data__(self, data: bytearray):
      crc_func = mkPredefinedCrcFun("modbus")
      crc_int = crc_func(data)
      crc = crc_int.to_bytes(2, "little")
      data.extend(crc)
      return data

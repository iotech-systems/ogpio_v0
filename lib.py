
import time, serial
from crcmod.predefined import *

"""
   intbuff = (0xff, 0x05, 0x00, 0x00, 0xFF, 0x00)
"""
def get_write_buff(unit: int, relay: int, val: int):
   buff: bytearray = bytearray()
   # -- modbus address --
   buff.append(unit)
   # -- modbus function --
   buff.append(0x05)
   # -- relay address --
   buff.extend([0, relay])
   if val == 1:
      buff.extend([0x00, 0x00])
   else:
      buff.extend([0xff, 0x00])
   return buff

def set_relay_state(ser: serial.Serial, unit_adr: int, relay: int, val: int):
   if not ser.isOpen():
      ser.open()
   if ser.isOpen():
      print("\n\t--[ Serial Port Is Opened! ]--\n")
   # -- run --
   data = get_write_buff(unit_adr, relay, val)
   outbuff = add_crc_data(data)
   send_buff(ser, outbuff)


"""
   Set the device address to 1
    00 10 00 00 00 01 02 00 01 6A 00
   Set the device address to 255
    00 10 00 00 00 01 02 00 FF EB 80
   The 9th byte of the sending frame, 0xFF, is the written device address
"""
def change_modbus_adr(ser: serial.Serial, new_adr: int):
   if not ser.isOpen():
      ser.open()
   if ser.isOpen():
      print("\n\t--[ Serial Port Is Opened! ]--\n")
   data: () = (0x00, 0x10, 0x00, 0x00, 0x00, 0x01, 0x02, 0x00)
   buff: bytearray = bytearray(data)
   buff.append(new_adr)
   buff = add_crc_data(buff)
   send_buff(ser, buff)


def add_crc_data(data: bytearray):
   crc_func = mkPredefinedCrcFun("modbus")
   crc_int = crc_func(data)
   crc = crc_int.to_bytes(2, "little")
   data.extend(crc)
   return data

def send_buff(ser: serial.Serial, outbuff: bytearray, ser_close: bool = True):
   print(f"sending: {outbuff}")
   ser.write(outbuff)
   ser.flush()
   time.sleep(0.02)
   # -- wait --
   while ser.in_waiting == 0:
      print(f"in_waiting: {ser.in_waiting}")
      time.sleep(0.01)
   # -- read --
   print(f"reading ~ in_waiting: {ser.in_waiting}")
   inbuff: bytearray = bytearray()
   while ser.in_waiting > 0:
      b = ser.read(1)
      inbuff.extend(b)
   # -- print --
   print(f"response: {inbuff}")
   if ser_close:
      ser.close()

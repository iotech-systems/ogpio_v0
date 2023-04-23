#!/usr/bin/env python3

import setproctitle
import serial, sys, time, os.path
from interfaces.modbusBoard import modbusBoard
from boards.lctech4chModbus import lctech4chModbus
from core.clock import clock
from core.sunclock import *
from utils.sysUtils import sysUtils
from datatypes.gpioState import gpioState
from datatypes.timetableXml import timetableXml
# from datatypes.modbusInfo import modbusInfo
from datatypes.modbusGPIO import modbusGPIO
from core.fileMonitor import fileMonitor
from datatypes.ttyDev import ttyDev


_src_file = sys.argv[0]
_timetable_xml: str = ""

if len(sys.argv) == 1:
   _timetable_xml = "rtmr_timetable.xml"
elif len(sys.argv) == 2:
   _timetable_xml = sys.argv[1]
else:
   print("-- [ bad argv ] --")
   exit(1)

if not os.path.exists(_timetable_xml):
   print(f"\n\t[ FileNotFound: {_timetable_xml} ]\n")
   exit(1)

SUN_DUMP_FILE: str = "/run/iotech/ogpio/sun.dump"
LOC_INFO: locationTxtInfo = locationTxtInfo("location.txt")
LOC_INFO.load()
GPIO_TIMETABLE: timetableXml = timetableXml(_timetable_xml, LOC_INFO)


def on_conf_change():
   print("on_conf_change")


fileMon: fileMonitor = fileMonitor(_timetable_xml)
fileMon.set_callback(None)
fileMon.start()
print(f"\n\n\t-- [ run-timer ] - -\n\t- - [ {_src_file} ] - -")

# -- make dir in /run --
run_iotech_gpio = "/run/iotech/ogpio"
if not os.path.exists(run_iotech_gpio):
   os.makedirs(run_iotech_gpio)
# -- --
if os.path.exists(run_iotech_gpio):
   print(f"PathFound: {run_iotech_gpio}")


def load_timetable_xml_file():
   if GPIO_TIMETABLE.load() != 0:
      print(f"UnableToLoadXmlFile: {_timetable_xml}")
      exit(1)
   # -- print tt --
   print(GPIO_TIMETABLE.pprint())

def main_loop():
   print("\n-- [ main_loop ] --\n")
   while True:
      try:
         # -- -- -- --
         rval: int = GPIO_TIMETABLE.reload()
         msg = ["FileNotChanged", "NewFileLoaded", "RunError"][rval]
         print(msg)
         # -- -- -- --
         with open(SUN_DUMP_FILE, "w") as f:
            f.write(GPIO_TIMETABLE.pprint())
         # -- -- -- --
         for dev in GPIO_TIMETABLE.MB_DEVICES:
            if dev.ttydev.dev in ["NotFound", "auto"]:
               continue
            ser: serial.Serial = serial.Serial(port=dev.ttydev.dev)
            board: lctech4chModbus = lctech4chModbus(ser, dev.mb_adr)
            for pin in dev.GPIOS:
               pin_state = gpioState(pin.on, pin.off)
               b_state = pin_state.calc_current_state(activeState=True)
               s_state = ""
               board.set_channel(pin.id, b_state)
         # -- -- -- --
      except Exception as e:
         print(e)
      finally:
         time.sleep(8.0)

def main():
   if GPIO_TIMETABLE.load() != 0:
      print(f"UnableToLoadXmlFile: {_timetable_xml}")
      exit(1)
   GPIO_TIMETABLE.update_mb_devices()
   main_loop()


# -- -- -- -- start  -- -- -- --
if __name__ == "__main__":
   PROC_NAME = "omms::ogpio"
   setproctitle.setproctitle(PROC_NAME)
   main()

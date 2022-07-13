
from core.sunclock import *
from core.clock import clock
from core.locationTxtInfo import *


class gpioState(object):

   def __init__(self, strOn: str, strOff: str):
      self.strOn: str = strOn
      self.strOff: str = strOff
      self.timeOn: datetime.time = self.__to_time__(self.strOn)
      self.timeOff: datetime.time = self.__to_time__(self.strOff)
      # self.locInfo = DEFAULT_LOC_INFO

   def calc_current_state(self, activeState: bool = True) -> bool:
      calc_val: bool = self.__calc_state__()
      return calc_val == activeState

   def __to_time__(self, tmStr: str) -> datetime.time:
      t: datetime.time
      if sunClock.is_sun_format(tmStr):
         sunClk = sunClock()
         t = sunClk.get_time_v1(tmStr)
      else:
         t = clock.get_time(tmStr)
      # -- return time --
      return t

   def __calc_state__(self) -> bool:
      # -- calc --
      time_now = datetime.datetime.now().time()
      # -- if in 24 hrs --
      if self.timeOn < self.timeOff:
         return self.timeOn < time_now < self.timeOff
      # -- if off next day --
      elif self.timeOff < self.timeOn:
         return (self.timeOn < time_now) or (time_now < self.timeOff)
      else:
         return False


# -- -- test -- --
if __name__ == "__main__":
   strOn = "11:45"; strOff = "sunrise+45"
   gpioCalc = gpioState(strOn, strOff)
   state: bool = gpioCalc.calc_current_state(activeState=True)
   print(f"state: {state}")

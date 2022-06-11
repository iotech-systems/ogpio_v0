
import datetime


class clock(object):

   @staticmethod
   def is_good_time(time_str: str) -> bool:
      arr = time_str.split(":")
      if len(arr) != 2:
         raise Exception("bad arr")
      hr: int = int(arr[0])
      mn: int = int(arr[1])
      if hr not in range(0, 24):
         raise Exception("bad hr")
      if mn not in range(0, 60):
         raise Exception("bad mn")
      return True

   @staticmethod
   def get_state(ont: str, oft: str):
      time_on: datetime.time = clock.get_time(ont)
      time_off: datetime.time = clock.get_time(oft)
      # -- calc --
      time_now = datetime.datetime.now().time()
      # -- if in 24 hrs --
      if time_on < time_off:
         return time_on < time_now < time_off
      # -- if off next day --
      elif time_off < time_on:
         return (time_on < time_now) or (time_now < time_off)
      else:
         return False

   @staticmethod
   def get_time(tme: str) -> datetime.time:
      hr, mn = tme.split(":")
      hr: int = int(hr)
      mn: int = int(mn)
      return datetime.time(hour=hr, minute=mn, second=0, microsecond=0)
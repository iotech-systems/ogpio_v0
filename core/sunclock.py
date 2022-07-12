
import re, pytz
import datetime, astral
from astral.sun import sun
from core.locationTxtInfo import locationTxtInfo


"""
   dawn, sunrise, noon, sunset, dusk
"""
DAY_PARTS = ("dawn", "sunrise", "noon", "sunset", "dusk")
RGX = r"(dawn|sunrise|noon|sunset|dusk)([\+|\-][0-9]{2})"
MAX_OFFSET = 59


class sunClock(object):

   def __init__(self, loc_info: locationTxtInfo):
      self.locInfo: locationTxtInfo = loc_info
      # -- set location --
      self.city = astral.LocationInfo(self.locInfo.location()
         , region=self.locInfo.region(), timezone=self.locInfo.tz()
         , latitude=self.locInfo.lat(), longitude=self.locInfo.lng())

   def get_time(self, day_part, offset: int = 0):
      # -- test max offset --
      if abs(offset) > MAX_OFFSET:
         raise Exception(f"BadMaxOffset: {offset}")
      # -- run --
      dt: datetime.datetime = self.get_datetime(day_part)
      delta = datetime.timedelta(minutes=offset)
      dt_delta = (dt + delta)
      print(f"dt: {dt} | dt_delta: {dt_delta} | offset: {offset}")
      return dt_delta.time()

   def get_time_v1(self, day_part: str):
      tm, offset = (day_part, 0)
      if "+" in day_part:
         tm, offset = day_part.split("+")
      elif "-" in day_part:
         tm, offset = day_part.split("-")
         offset = f"-{offset}"
      # -- --
      return self.get_time(tm, int(offset))

   def get_datetime(self, day_part) -> datetime.datetime:
      if day_part not in DAY_PARTS:
         raise Exception(f"bad day_part: {day_part}")
      # -- look up day part --
      today = datetime.date.today()
      __sun = sun(observer=self.city.observer, date=today,
         tzinfo=pytz.timezone(self.locInfo.tz()))
      dt: datetime.datetime = __sun[day_part]
      return dt.replace(second=0).replace(microsecond=0)

   def __str__(self):
      # ("dawn", "sunrise", "noon", "sunset", "dusk")
      dw = self.get_time_v1("dawn")
      sr = self.get_time_v1("sunrise")
      nn = self.get_time_v1("noon")
      ss = self.get_time_v1("sunset")
      dk = self.get_time_v1("dusk")
      return f"SUN: [ down: {dw} | sunrise: {sr} | noon: {nn} | sunset: {ss} | dusk: {dk} ]"

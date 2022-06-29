
import re, pytz
import datetime, astral
from astral.sun import sun
from core.locationTxtInfo import locationTxtInfo


"""
   dawn, sunrise, noon, sunset, dusk
"""
DAY_PARTS = ("dawn", "sunrise", "noon", "sunset", "dusk")
RGX = r"(dawn|sunrise|noon|sunset|dusk)([\+|\-][0-9]{2})"


class sunClock(object):

   def __init__(self, loc_info: locationTxtInfo):
      self.locInfo: locationTxtInfo = loc_info
      # -- set location --
      self.city = astral.LocationInfo(self.locInfo.location()
         , region=self.locInfo.region(), timezone=self.locInfo.tz()
         , latitude=self.locInfo.lat(), longitude=self.locInfo.lng())

   def get_time(self, day_part, offset: int = 0):
      dt: datetime.datetime = self.get_datetime(day_part)
      delta = datetime.timedelta(minutes=offset)
      dt_delta = (dt + delta)
      print(f"dt: {dt} | dt_delta: {dt_delta} | offset: {offset}")
      return dt_delta.time()

   def get_datetime(self, day_part) -> datetime.datetime:
      if day_part not in DAY_PARTS:
         raise Exception(f"bad day_part: {day_part}")
      # -- look up day part --
      today = datetime.date.today()
      __sun = sun(observer=self.city.observer, date=today,
         tzinfo=pytz.timezone(self.locInfo.tz()))
      dt: datetime.datetime = __sun[day_part]
      return dt.replace(second=0).replace(microsecond=0)

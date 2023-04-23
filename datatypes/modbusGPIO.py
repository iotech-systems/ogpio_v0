import calendar
import datetime
import xml.etree.ElementTree as et
from datatypes.datatypes import scheduleItem


class modbusGPIO(object):

   def __init__(self, e: et.Element):
      self.id: int = int(e.attrib["id"])
      self.lbl: str = e.attrib["lbl"]
      self.enabled: bool = (e.attrib["enabled"] in ["on", "ON", "1"])
      self.note: str = e.attrib["note"]
      self.schedule: list[scheduleItem] = []
      self.__load_schedule__(e)

   def schedule_item_today(self) -> [None, scheduleItem]:
      week_day_index = datetime.datetime.today().weekday()
      day_name = calendar.day_name[week_day_index]
      items = [i for i in self.schedule if i.day == day_name]
      if len(items) == 1:
         return items[0]
      else:
         return None

   def __load_schedule__(self, e: et.Element):
      try:
         xpath = "schedule/item"
         items: [] = e.findall(xpath)
         for i in items:
            self.schedule.append(scheduleItem(i))
      except Exception as e:
         print(e)

   def __str__(self):
      schedule: str = "".join([f"\t\t\t{str(s)}\n" for s in self.schedule])
      return f"\tgpio enabled: {self.enabled} | id: {self.id} | lbl: {self.lbl} |" \
         f" note: {self.note}\n{schedule}"

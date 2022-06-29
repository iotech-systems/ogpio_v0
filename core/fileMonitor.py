
import os, threading
import time


class fileMonitor(object):

   def __init__(self, path: str):
      self.path = path
      self.__prev_stamp__ = 0
      self.__callback__ = None
      self.run_flag = True
      self.file_changed: bool = False
      self.extFileChangeFlag: bool = False
      self.__thr = threading.Thread(target=self.__mon_file__)

   def start(self):
      if not os.path.exists(self.path):
         raise FileExistsError(f"PathNotFound: {self.path}")
      self.__prev_stamp__ = os.stat(self.path).st_mtime
      self.__thr.start()

   def stop(self):
      self.run_flag = False

   def set_callback(self, callback):
      self.__callback__ = callback

   def __mon_file__(self):
      while self.run_flag:
         try:
            stamp = os.stat(self.path).st_mtime
            if stamp != self.__prev_stamp__:
               self.__prev_stamp__ = stamp
               self.file_changed = True
               self.extFileChangeFlag = True
               if self.__callback__ is None:
                  print(f"PathChangeEvent: {self.path}")
               else:
                  self.__callback__()
            else:
               self.file_changed = False
         except Exception as e:
            print(e)
         finally:
            time.sleep(2.0)
      # -- exit/stop --
      print("exit/stop::__mon_file__")
